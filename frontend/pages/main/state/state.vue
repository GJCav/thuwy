<template>
	<view class="container">
		<weiyang-card :text="text" :color="color"></weiyang-card>
		<weiyang-card></weiyang-card>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				text:{
					title: '从游坊第20讲',
					corner: '已报名25/20',
					theme: '张三老师：关于怎么躺平的介绍',
					content: '4月20日 12：00南区9号楼地下活动空间，不见不散！',
					info: '2022-4-18 23：59 截止',
					tag: '可报名'
				},
				color:['#DAF3ED','#45C5A6','#37806F']
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
