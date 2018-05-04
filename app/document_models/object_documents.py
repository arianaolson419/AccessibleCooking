""" Contains objects and object fields for
equipment, ingredients, and instructions """

from flask_mongoalchemy import *
from .tip_documents import Tip
from app import db

class TippedEntry(object):
    """ Entry in the recipe that can point to a tip.
    Contains the text and related tips.
    """
    def __init__(self, line, tip_id=None, tip_name=None):
        self.text = line
        self.tip_id = tip_id
        self.tip_name = tip_name

    def set_tip(self, tip_id, tip_name):
        self.tip_id = tip_id
        self.tip_name = tip_name

    def give_tip_link(self):
        if self.tip_id:
            return "/tip/" + self.tip_id
        return ""

    def has_tip(self):
        if self.tip_id: return True
        return False

    def recommend_tips(self):
        pass

class Ingredient(TippedEntry):
    def recommend_tips(self):
        word_list = self.text.split()
        return Tip.query.filter({'tags':{'$in':['ingredient']}})#,
                                # 'ingredients':{'$in':word_list}})

class Equipment(TippedEntry):
    def recommend_tips(self):
        word_list = self.text.split()
        return Tip.query.filter({'tags':{'$in':['equipment']}})#,
                                # 'equipment':{'$in':word_list}})

class Instruction(TippedEntry):
    def recommend_tips(self):
        word_list = self.text.split()
        return Tip.query.filter({'tags':{'$in':['method']}})#,
                                # 'instructions':{'$in':word_list}})

class TippedEntryField(db.Field):
    def __init__(self, **kwargs):
        super(TippedEntryField, self).__init__(**kwargs)

    def schema_json(self):
        super_schema = super(TippedEntryField, self).schema_json()
        return dict(**super_schema)

    def validate_wrap(self, value):
        """ Checks that the correct number of elements are in ``value`` and that
            each element validates agains the associated Field class
        """
        if not isinstance(value, TippedEntry):
            self._fail_validation_type(value, TippedEntry)

    def validate_unwrap(self, value):
        assert value['_type'] in ["Ingredient", "Equipment", "Instruction"]

    def wrap(self, value):
        self.validate_wrap(value)
        return {"_type":type(value).__name__, "text":value.text, 'tip_id':value.tip_id, 'tip_name':value.tip_name}

    def unwrap(self, value):
        mapping = {"Ingredient":Ingredient,
                    "Equipment":Equipment,
                    "Instruction":Instruction}
        self.validate_unwrap(value)
        return mapping[value['_type']](value['text'], value['tip_id'], value['tip_name'])
