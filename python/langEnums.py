from enum import Enum

class Exceptions(Enum):
	InvalidSyntax	= 100
	AlreadyDefined	= 101
	NotImplementedException	= 102
	NotDefinedException		= 103
	GeneralException		= 104
	DivideByZeroException	= 105
	InvalidValue			= 106
	InvalidTypeException	= 107

class Types(Enum):
	Boolean = 0
	Integer = 1
	Float	= 2
	List	= 3
	Dictionary = 4
	Tuple	= 5
	Dynamic	= 6
	String	= 7
	Any		= 8

class ConditionType(Enum):
	And	= 0
	Or	= 1
	Single	= 2