# cpp-core-model-builder

Model builder written in python for building YCTech C++ Core .h, .cc, .java and its JNI files.


# Usage:
python model-builder.py lesschat-model-description.xml


# Grammar:
1. group name should be "user_group".

2. class name should be "UserGroup".

3. variable name should be all lower cases with underscore. There are some attributes you must set in variable:
  - name
  - type : can be 'string', 'bool', 'int', '[string]', 'time'
           or 'enum', iff you specify the type is enum, you shuold add "enum" attribute to declare the enum class.
  - json_path (eg: 'data/uid'), if the attribute does not have json mapping, you should set an empty string rather than leaving blank (eg: '').
  - [maybe] enum : only affects when type='enum'
  - [maybe] sql_flag can be 'primary_key'
  - [maybe] json_search_path : if the attribute is '[string]', you can use json_search_path to find the key inside array objects.

4. enum name should be 'Role' (the first letter is upper case), alias should be ALL_UPPER_CASE.

5. manager name should be 'UserManager' (CRUD)
  - <save/> supports "singular"(SaveObjectToCache) and "plural"(SaveObjectsToCache)
  - <fetch/> supports "singular"(FetchObjectFromCache) , "plural"(FetchObjectsFromCache) , "by" (FetchObjectFromCacheById), "sort" (means sort by key name) and "desc" (default is ascending, if you set desc='true', will sort as decending).
  - <delete/> supports "singular"(DeleteObjectFromCache) and "plural"(DeleteObjectsFromCache) and "by" (DeleteObjectFromCacheById)
  - <update/> is not supported in version 1.0
  - WARNING: DO NOT use '[string]' variable as "by" filter

6. Since 3.0, you can use model-builder to generate WebApi and cache methods by using <api/>:
  - name : Name of WebApi
  - alias : Name of same Api in manager
  - method : can be one of "GET", "POST", "PUT", "DELETE"
  - uri : URI after host, often starts with "/api"
  - <inputs/> : You can put <variable/> here, but there are some additional meanings you should know:
    - json_path : Model-builder will use json_path as json11 "ToJson" path
    - capture : If you set capture='true', C++ will capture this property in lambda method
  - <outputs/> : You can put <variable/> here to delare vars in callback, but there are some additional meanings you should know:
    - json_path : Model-builder will use json_path to call object(s) "InitWithJsonOrDie" method.
    - cache : There are 2 kinds of methods you can use, command and define.
      - command : eg: save_plure_(id, task_id)
        - The first component is verb, you can use "save" or "delete" or "fupdate" or their plure words "saves", "deletes"
        - The second component is to tell the builder parameters to pass, will use the <variable/> name if not defined.
          *WARNING:
          save: If you use "save" or "saves", this component should leave blank.
          delete: If you set cache as "delete(task_id)", "this->DeleteTaskFromCacheByTaskId(task_id)" will be generated.
          fupdate: If you are using "fake update", it will fetch object from cache and set object's property and finally save the updated object to cache.
            It should be "fupdate:task_id(uid)", :task_id means "FetchTaskFromCacheByTaskId"
      - define : There indeed sometimes you cannot find suitable method to call in cache, we provide a tempory ability by introducing <define name='id' description='c++_method'/>, you can refer to "task_module.xml" for details, if you want to use define, you should put pound(#) in front of the define name (eg: #id)
      - You can enqueue cache tasks by comma, eg: cache='save_plure,#some_define'

# Licence
MIT
