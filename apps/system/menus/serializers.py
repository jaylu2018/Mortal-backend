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
        children_data = validated_data.pop("children", [])
        menu = Menu.objects.create(**validated_data)
        for child_data in children_data:
            Menu.objects.create(parent=menu, **child_data)
        return menu

    def update(self, instance, validated_data):
        children_data = validated_data.pop("children", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if children_data:
            for child_data in children_data:
                child_id = child_data.get("id")
                if child_id:
                    child = Menu.objects.filter(id=child_id).first()
                    if child:
                        for child_attr, child_value in child_data.items():
                            setattr(child, child_attr, child_value)
                        child.save()

        instance.save()
        return instance
