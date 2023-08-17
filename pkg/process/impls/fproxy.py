class Proxy:

    funcs: list


    def __init__(self, funcs: list):
        self.funcs = funcs

    def prompt(self, user_prompt: str):
        if len(self.funcs) == 0:
            return user_prompt
        
        raw = \
"""
# You now have access to the following functions:

```yaml
{functions}```

# P.S.
- `required` means the arguments are required.

# If user's input matches the description of a certain function, please output with following format to call the function:

```json
{{"name": "function_name", "args": {{"arg_name": "arg_value", ...}}}}
```

# If not, you can reply in your own way.

# User's input:
{user_prompt}

# Your output:
""".strip()
        funcs = ""
        for i in range(len(self.funcs)):
            # - name: func_name
            #   description: func_description
            #   args:
            #     - name: arg_name
            #       description: arg_description
            #       type: int
            #     - name: arg_name
            #       description: arg_description
            #       type: str
            #   required: [arg_name, ...]
            #   return: return_type
            func = self.funcs[i]

            func_desc = func['description'].replace("\n", "")

            args = ""

            for arg in func['parameters']['properties']:
                args += \
f"""    - name: {arg}
      description: {func['parameters']['properties'][arg]['description']}
      type: {func['parameters']['properties'][arg]['type']}
"""
            if args.endswith("\n"):
                args = args[:-1]

            func_str = \
f"""- name: {func['name']}
  description: {func_desc}
  args:
{args}
  required: {str(func['parameters']['required'])}
"""
            funcs += func_str
        return raw.format(functions=funcs, user_prompt=user_prompt)

    def call(self, func_name: str, args: dict) -> tuple[bool, str, any]:
        for func in self.funcs:
            if func['name'] == func_name:
                return func['function'](**args)
        return "error: no such function"
    
    def extra_function_call(self, text: str):
        """Extra function call request from text
        
        ```json
{
  "name": "access_web",
  "args": {
    "link": "https://www.example.com/search?q=RockChinQ"
  }
}
```
        """
        import re
        import json

        # 用正则提取json数据
        # 直接找大括号包围的, 匹配全文，不限于一行内
        json_strs = re.findall(r"\{.*\}", text, re.S)

        func_name = None
        args = None

        found = False

        # 逐个检查json数据是否符合格式
        for json_str in json_strs:
            try:
                # 删除所有// xxx
                json_str = re.sub(r"//.*", "", json_str)
                
                json_data = json.loads(json_str)
                func_name = json_data['name']
                args = json_data['args']
                found = True
                break
            except:
                continue
          
        if not found:
            return False, None, None

        return True, func_name, args