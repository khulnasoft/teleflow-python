"""This module is used to gather enumerations related to the Template resource in Teleflow"""

from teleflow.enums.polyfill import StrEnum


class TemplateVariableTypeEnum(StrEnum):
    """This enumeration define possible type for a variable in a template"""

    STRING = "String"
    """String variable"""

    LIST = "Array"
    """List variable"""

    BOOL = "Boolean"
    """Boolean variable"""
