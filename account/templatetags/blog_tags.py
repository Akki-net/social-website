from django import template
from ..models import Post
register = template.Library()
@register.simple_tag
def getCategory(cat):
    inx = Post.Category.values.index(cat)
    return Post.Category.labels[inx]