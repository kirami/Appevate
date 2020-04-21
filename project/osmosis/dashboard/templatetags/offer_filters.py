from django import template
import logging
logger = logging.getLogger("django") 
import math
from decimal import *

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
  return range(start, len(end))

@register.filter(name='index')
def index(List, i):
    return List[i]

@register.filter(name='modulo')
def modulo(num, val):
    return num % val

@register.filter(name='getDollars')
def getDollars(num):    
	split_num = str(num).split('.')
	if len(split_num) > 0:
		int_part = int(split_num[0])
		return int_part
	return split_num

@register.filter(name='getCents')
def getCents(num):
	split_num = str(num).split('.')	
	if len(split_num) > 1:
		return int(split_num[1])
	return "00"
	