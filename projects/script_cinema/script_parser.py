from ruamel.yaml import YAML
from typing import List, Dict
from copy import deepcopy

yaml = YAML(typ='safe')

class ParseStoryException(Exception):
    def __init__(self, message):
        self.message = message


class SingleDialog:
    def __init__(self, speaker: str, content: str, delay: int):
        self.speaker = speaker
        self.content = content
        self.delay = int(delay)

    def __repr__(self) -> str:
        return f'{self.speaker}: {self.content}\nDelay: {self.delay}'

    def __str__(self) -> str:
        return self.__repr__()


class Avatar:
    def __init__(self, key: str, name: str, image: str):
        self.key = key
        self.name = name
        self.image = image

    def __repr__(self) -> str:
        return f'{self.key} - {self.name} - {self.image}'

    def __str__(self) -> str:
        return self.__repr__()


class ChoiceConstraint:
    def __init__(self, key: str, min_value: int, max_value: int):
        self.key = key
        self.min_value = int(min_value)
        self.max_value = int(max_value)

    def __repr__(self) -> str:
        return f'{self.key}: {self.min_value} - {self.max_value}'

    def __str__(self) -> str:
        return self.__repr__()


class ChoiceValueChange:
    def __init__(self, key: str, value: int):
        self.key = key
        self.value = int(value)

    def __repr__(self) -> str:
        return f'{self.key}: {self.value:+d}'

    def __str__(self) -> str:
        return self.__repr__()


class SingleChoice:
    def __init__(self, name: str, goto: str):
        self.name = name
        self.goto = goto
        self.constraint: Dict[str, ChoiceConstraint] = {}
        self.value_change: Dict[str, ChoiceValueChange] = {}

    def add_constraint(self, constraint: ChoiceConstraint):
        self.constraint[constraint.key] = constraint

    def check_constraint(self, values: dict):
        for value_name, value in values.items():
            if value_name in self.constraint:
                constraint = self.constraint[value_name]
                if value < constraint.min_value or value > constraint.max_value:
                    return False
        return True

    def add_value_change(self, value_change: ChoiceValueChange):
        self.value_change[value_change.key] = value_change

    def apply_value_change(self, values: dict):
        for value_name, value in values.items():
            if value_name in self.value_change:
                value_change = self.value_change[value_name]
                values[value_change.key] = value + value_change.value
        return values

    def __repr__(self) -> str:
        return f'{self.name} - {self.goto}'

    def __str__(self) -> str:
        return self.__repr__()


class StoryUnit:
    def __init__(self, key: str, default_next: str, is_end: bool = False):
        self.key = key
        self.default_next = default_next
        self.is_end = is_end
        self.member: List[Avatar] = []
        self.dialog: List[SingleDialog] = []
        self.choice: List[SingleChoice] = []

    def add_member(self, member: Avatar):
        self.member.append(member)

    def add_dialog(self, dialog: SingleDialog):
        self.dialog.append(dialog)

    def add_choice(self, choice: SingleChoice):
        self.choice.append(choice)

    def __repr__(self) -> str:
        return f'{self.key} - {self.default_next} - {self.is_end}'

    def __str__(self) -> str:
        return self.__repr__()


class Story:
    def __init__(self):
        self.story: Dict[str, StoryUnit] = {}
        self.avatar: Dict[str, Avatar] = {}
        self.property: Dict[str, int] = {}
        self.global_property: Dict[str, int] = {}
        self.start_unit: str = None

    def add_story_unit(self, story_unit: StoryUnit):
        self.story[story_unit.key] = story_unit

    def add_avatar(self, avatar: Avatar):
        self.avatar[avatar.key] = avatar

    def parse_yaml(self, story_yaml: Dict):
        try:
            self.start_unit = story_yaml['start']
            avatars: Dict = story_yaml['avatar']
            properties: Dict = story_yaml['property']
            global_properties: Dict = story_yaml['global']
            story_units: Dict = story_yaml['act']
        except KeyError as e:
            raise ParseStoryException('story yaml is not valid, error: {e}')
        for avatar_key, avatar_value in avatars.items():
            try:
                avatar = Avatar(
                    avatar_key, avatar_value['name'], avatar_value['image'])
                self.add_avatar(avatar)
            except KeyError:
                raise ParseStoryException(f'avatar {avatar_key} is not valid')
        for property_key, property_value in properties.items():
            try:
                self.property[property_key] = int(property_value)
            except ValueError:
                raise ParseStoryException(
                    f'property {property_key} is not valid')
        for global_key, global_value in global_properties.items():
            try:
                self.global_property[global_key] = int(global_value)
            except ValueError:
                raise ParseStoryException(
                    f'global property {global_key} is not valid')
        try:
            for act_key, act_value in story_units.items():
                try:
                    story_unit = StoryUnit(
                        act_key, act_value['default'], act_value.get('end', False))
                except KeyError:
                    raise ParseStoryException(
                        f'act {act_key} default next is not defined')
                if story_unit.default_next and story_unit.default_next not in story_units:
                    raise ParseStoryException(
                        f'act {act_key} default next is not any unit')
                if not story_unit.is_end and not story_unit.default_next:
                    raise ParseStoryException(
                        f'act {act_key} is not end and has no default next')
                for member in act_value['member']:
                    if member not in self.avatar:
                        raise ParseStoryException(
                            f'avatar {member} in act {act_key} is not defined')
                    try:
                        story_unit.add_member(self.avatar[member])
                    except KeyError:
                        raise ParseStoryException(
                            f'avatar {member} in act {act_key} is not defined')
                for dialog in act_value['dialog']:
                    try:
                        story_unit.add_dialog(SingleDialog(
                            dialog['speaker'], dialog['content'], dialog['delay']))
                    except KeyError:
                        raise ParseStoryException(
                            f'dialog in act {act_key} is not valid')
                    if dialog['speaker'] not in self.avatar:
                        raise ParseStoryException(
                            f'dialog in act {act_key} has invalid speaker {dialog["speaker"]}')
                if 'choice' in act_value and act_value['choice'] and len(act_value['choice']) > 0:
                    for choice in act_value['choice']:
                        single_choice = SingleChoice(
                            choice['name'], choice['goto'])
                        constraints: Dict[str, Dict[str, int]
                                          ] = choice.get('constraint', {})
                        if constraints and len(constraints) > 0:
                            for constraint_name, constraint_minmax in constraints.items():
                                if constraint_name not in self.property and constraint_name not in self.global_property:
                                    raise ParseStoryException(
                                        f'choice in act {act_key} has invalid constraint {constraint_name}')
                                constraint_minmax: Dict[str,
                                                        int] = constraint_minmax
                                try:
                                    constraint = ChoiceConstraint(constraint_name, constraint_minmax.get(
                                        'min', -99999999), constraint_minmax.get('max', 99999999))
                                except ValueError:
                                    raise ParseStoryException(
                                        f'choice in act {act_key} has invalid constraint {constraint_name}')
                                single_choice.add_constraint(constraint)
                        value_changes: Dict[str, int] = choice.get('value', {})
                        if value_changes and len(value_changes) > 0:
                            for value_name, value_change in value_changes.items():
                                if value_name not in self.property and value_name not in self.global_property:
                                    raise ParseStoryException(
                                        f'choice in act {act_key} has invalid value {value_name}')
                                value_change: Dict[str, int] = value_change
                                try:
                                    value_change = ChoiceValueChange(
                                        value_name, value_change)
                                except ValueError:
                                    raise ParseStoryException(
                                        f'choice in act {act_key} has invalid value {value_name}')
                                single_choice.add_value_change(value_change)
                        story_unit.add_choice(single_choice)
                self.add_story_unit(story_unit)
        except KeyError as e:
            raise ParseStoryException(
                f'act {act_key} is not valid, error: {e}')
        if self.start_unit not in self.story:
            raise ParseStoryException(
                f'start unit {self.start_unit} is not any unit')
    
    def get_init_value(self) -> (Dict[str, int], Dict[str, int]):
        return deepcopy(self.property), deepcopy(self.global_property)
    
    def startunit(self) -> StoryUnit:
        return self.story[self.start_unit]

    def __repr__(self) -> str:
        return f'{self.story}\n{self.avatar}\n{self.property}\n{self.global_property}\n{self.start_unit}'

    def __str__(self) -> str:
        return self.__repr__()


def parse_story(path: str) -> Story:
    story_map = None
    with open(path) as f:
        story_map = yaml.load(f)
    story = Story()
    story.parse_yaml(story_map)
    return story

if __name__ == '__main__':
    story = parse_story('mahjong.yaml')
    print(story.story)
    print(story.avatar)
    print(story.property)
    print(story.global_property)
    print(story.start_unit)
    print(story.story['stage3'].choice[2].constraint['active_loss'])

