from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
# Create your models here.

class GoodType(BaseModel):
    '''商品类型模型类'''
    name = models.CharField(max_length=20,verbose_name="种类名称")
    logo = models.CharField(max_length=20,verbose_name="标识")
    image = models.ImageField(upload_to='type',verbose_name="商品类型图片")

    class Meta:
        db_table = "j_goods_type"
        verbose_name = "商品种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(BaseModel):
    '''商品SKU模型类'''
    status_choices = (
        (0,'线下'),
        (1,'线上')
    )
    type = models.ForeignKey('GoodType',verbose_name="商品种类",on_delete=models.DO_NOTHING)
    goods = models.ForeignKey('Goods',verbose_name="商品SPU",on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20,verbose_name="商品名称")
    desc = models.CharField(max_length=256,verbose_name="商品简介")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="价钱")
    unite = models.CharField(max_length=20,verbose_name="商品单位")
    image = models.ImageField(upload_to='goods',verbose_name="商品图片")
    stock = models.IntegerField(default=1,verbose_name="商品库存")
    sales = models.IntegerField(default=0,verbose_name="商品销量")
    status = models.SmallIntegerField(default=1,choices=status_choices,verbose_name="状态")

    class Meta:
        db_table = 'j_goods_sku',
        verbose_name = '商品',
        verbose_name_plural = verbose_name

class Goods(BaseModel):
    '''商品SPU模型类'''
    name = models.CharField(max_length=20,verbose_name="商品SPU名称")
    #富文本类型，带有格式文本
    detail = HTMLField(blank=True,verbose_name="商品详情")

    class Meta:
        db_table = 'j_goods',
        verbose_name = '商品SPU',
        verbose_name_plural = verbose_name

class GoodsImage(BaseModel):
    '''商品图片模型类'''
    sku = models.ForeignKey('GoodsSKU',verbose_name="商品",on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='goods',verbose_name="图片路径")

    class Meta:
        db_table = 'j_goods_image',
        verbose_name = "商品图片",
        verbose_name_plural = verbose_name

class IndexGoodsBanner(BaseModel):
    '''首页轮播商品类展示模型'''
    sku = models.ForeignKey('GoodsSKU',verbose_name="商品",on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='banner',verbose_name="图片")
    index = models.SmallIntegerField(default=0,verbose_name="展示顺序")

    class Meta:
        db_table = 'j_index_promotion',
        verbose_name = '主页促销活动',
        verbose_name_plural = verbose_name
