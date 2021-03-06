from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)

from ecoke.models import Brand

# hyperlink to detail view
brand_detail_url = HyperlinkedIdentityField(
    view_name='api:detail',
    lookup_field='pk',
)
# hyperlink to update view
brand_update_url = HyperlinkedIdentityField(
    view_name='api:update',
    lookup_field='pk',
)
# hyperlink to delete view
brand_delete_url = HyperlinkedIdentityField(
    view_name='api:delete',
    lookup_field='pk',
)


class BrandDetailsSerializer(ModelSerializer):
    """Serializer to map the MOdel instance into JSON format."""
    class Meta:
        model = Brand
        fields = (
            'collector_name',
            'respondent_name',
            'respondent_city',
            'favourite_drink',
            'date_of_collection',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


class BrandCreateSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'collector_name',
            'respondent_name',
            'respondent_city',
            'favourite_drink',
            'date_of_collection'
        ]


class BrandListSerializer(ModelSerializer):
    url = brand_detail_url
    delete_url = brand_delete_url

    class Meta:
        model = Brand
        fields = [
            'url',
            'collector_name',
            'respondent_name',
            'respondent_city',
            'favourite_drink',
            'date_of_collection',
            'delete_url'
        ]


class BrandRetrieveSerializer(ModelSerializer):
    update_url = brand_update_url

    class Meta:
        model = Brand
        fields = [
            'id',
            'collector_name',
            'respondent_name',
            'respondent_city',
            'favourite_drink',
            'date_of_collection',
            'update_url'
        ]
        read_only_fields = ('date_created', 'date_modified')
