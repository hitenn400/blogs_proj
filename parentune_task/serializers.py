from rest_framework import serializers
from .models import AgeGroup, ParentInfo, ChildInfo, Blogs

class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ['id', 'age_range']

class BlogsSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    suitable_for_age = AgeGroupSerializer(many=True)

    class Meta:
        model = Blogs
        fields = '__all__'

    def create(self, validated_data):
        age_groups_data = validated_data.pop('suitable_for_age')
        blog = Blogs.objects.create(**validated_data)
        for age_group_data in age_groups_data:
            age_group, created = AgeGroup.objects.get_or_create(**age_group_data)
            blog.suitable_for_age.add(age_group)
        return blog

    def update(self, instance, validated_data):
        age_groups_data = validated_data.pop('suitable_for_age')
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.suitable_for_gender = validated_data.get('suitable_for_gender', instance.suitable_for_gender)
        instance.save()

        instance.suitable_for_age.clear()
        for age_group_data in age_groups_data:
            age_group, created = AgeGroup.objects.get_or_create(**age_group_data)
            instance.suitable_for_age.add(age_group)

        return instance

class ParentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentInfo
        fields = '__all__'


class ChildInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildInfo
        fields = '__all__'


