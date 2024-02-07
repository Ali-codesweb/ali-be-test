from rest_framework import serializers


class Validator(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        fields: dict = kwargs.pop('fields', None)
        data = kwargs.pop('data', None)
        self.fields_list = []
        super(Validator, self).__init__(data=data, *args, **kwargs)
        if fields:
            for k, v in fields.items():
                self.fields[k] = v
                self.fields_list.append(k)
        self.is_valid(raise_exception=True)

    def __new__(cls, *args, **kwargs):
        instance = super(Validator, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        data = {}
        for field_name in instance.fields_list:
            data[field_name] = instance.validated_data.get(field_name)
        return data.values()
