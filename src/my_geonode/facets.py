from geonode.facets.models import FacetProvider, DEFAULT_FACET_PAGE_SIZE


class GroupFacetProvider(FacetProvider):
    FACET_NAME = "group"

    def get_info(self, lang="en"):
        return {
            "name": self.FACET_NAME,
            "key": "group__slug",
            "label": "Group",
            "localized_label": "Group",
            "type": "group",
            "hierarchical": False,
            "order": 5,
        }

    def get_facet_items(self, queryset, start=0, end=DEFAULT_FACET_PAGE_SIZE, lang="en", topic_contains=None):
        from geonode.groups.models import GroupProfile
        from django.db.models import Count
        qs = GroupProfile.objects.filter(group__resourcebase__isnull=False).annotate(count=Count("group__resourcebase", distinct=True)).order_by("-count")
        if topic_contains:
            qs = qs.filter(title__icontains=topic_contains)
        total = qs.count()
        return total, [{"key": g.slug, "label": g.title, "localized_label": g.title, "count": g.count} for g in qs[start:end]]

    @classmethod
    def register(cls, registry, **kwargs):
        registry.register_facet_provider(cls())


class GroupCategoryFacetProvider(FacetProvider):
    FACET_NAME = "group_category"

    def get_info(self, lang="en"):
        return {
            "name": self.FACET_NAME,
            "key": "group__groupprofile__categories__slug",
            "label": "Theme",
            "localized_label": "Theme",
            "type": "group_category",
            "hierarchical": False,
            "order": 4,
        }

    def get_facet_items(self, queryset, start=0, end=DEFAULT_FACET_PAGE_SIZE, lang="en", topic_contains=None):
        from geonode.groups.models import GroupCategory
        from django.db.models import Count
        qs = GroupCategory.objects.filter(groupprofile__group__resourcebase__isnull=False).annotate(count=Count("groupprofile__group__resourcebase", distinct=True)).order_by("name")
        if topic_contains:
            qs = qs.filter(name__icontains=topic_contains)
        total = qs.count()
        return total, [{"key": c.slug, "label": c.name, "localized_label": c.name, "count": c.count} for c in qs[start:end]]

    @classmethod
    def register(cls, registry, **kwargs):
        registry.register_facet_provider(cls())
