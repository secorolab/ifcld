class Param:
    @staticmethod
    def is_reference(param):
        return param.startswith("#") and param[1:].isdigit()

    @staticmethod
    def is_null(param):
        return param == "$"

    @staticmethod
    def is_derivable(param):
        return param == "*"

    @staticmethod
    def is_boolean(param):
        return param in [".T.", ".F."]

    @staticmethod
    def is_enum(param):
        return isinstance(param, str) and param.startswith(".") and param.endswith(".")
