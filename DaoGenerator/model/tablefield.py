
class TableFieldModel(object):
    '''
    classdocs
    '''


    def __init__(self , field_name = '' , data_type = '' , is_primary_key = '' , auto_increment = '' , length = 0 , is_foreign_key_constraint = '' , foreign_key_name = '' , foreign_key_table = ''):
        self._fieldName = field_name
        self._dataType = data_type
        self._isPrimaryKey = is_primary_key
        self._autoIncrement = auto_increment
        self._length = length
        self._isForeignKeyConstraint = is_foreign_key_constraint
        self._foreignKeyName = foreign_key_name
        self._foreignKeyTable = foreign_key_table
        
    @property
    def fieldName(self):
        return self._fieldName
    
    @fieldName.setter
    def fieldName(self , value):
        self._fieldName = value

    @property
    def dataType(self):
        return self._dataType
    
    @dataType.setter
    def dataType(self , value):
        self._dataType = value
        
    @property
    def isPrimaryKey(self):
        return self._isPrimaryKey
    
    @isPrimaryKey.setter
    def isPrimaryKey(self , value):
        self._isPrimaryKey = value
    
    @property
    def autoIncrement(self):
        return self._autoIncrement
    
    @autoIncrement.setter
    def autoIncrement(self , value):
        self._autoIncrement = value
    
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self , value):
        self._length = value
    
    @property
    def isForeignKeyConstraint(self):
        return self._isForeignKeyConstraint
    
    @isForeignKeyConstraint.setter
    def isForeignKeyConstraint(self , value):
        self._isForeignKeyConstraint = value
        
    @property
    def foreignKeyName(self):
        return self._foreignKeyName
    
    @foreignKeyName.setter
    def foreignKeyName(self , value):
        self._foreignKeyName = value
        
    @property
    def foreignKeyTable(self):
        return self._foreignKeyTable
    
    @foreignKeyTable.setter
    def foreignKeyTable(self , value):
        self._foreignKeyTable = value
    
        