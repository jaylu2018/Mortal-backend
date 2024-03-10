from rest_framework import serializers
from .models import Menu


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MenuSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Menu
        fields = "__all__"

    def create(self, validated_data):
        children_data = validated_data.pop("children", None)
        menu = Menu.objects.create(**validated_data)
        if children_data is not None:
            for child_data in children_data:
                Menu.objects.create(parent=menu, **child_data)
        return menu

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "children":
                for child_data in value:
                    child_id = child_data.get("id", None)
                    if child_id:
                        try:
                            child = Menu.objects.get(id=child_id)
                            for child_attr, child_value in child_data.items():
                                setattr(child, child_attr, child_value)
                            child.save()
                        except Menu.DoesNotExist:
                            pass
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance
