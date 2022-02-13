<template>
	<view class="container">
		<view v-for="item in sample">
			<weiyang-card :text="item.text" :color="item.color" :pic="item.pic"></weiyang-card>
		</view>
		<weiyang-card></weiyang-card>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				sample:[
					{
						text:{
							title: '从游坊第20讲',
							corner: '已报名25/20',
							theme: '张三老师：关于怎么躺平的介绍',
							content: '4月20日 12：00南区9号楼地下活动空间，不见不散！',
							info: '2022-4-18 23：59 截止',
							tag: '可报名'
						},
						pic:'reserve.svg',
						color:['#DAF3ED','#45C5A6','#37806F']
					},
					{
						text:{
							title: '从游坊第20讲',
							corner: '已报名25/20',
							theme: '张三老师：关于怎么躺平的介绍',
							content: '4月20日 12：00南区9号楼地下活动空间，不见不散！',
							info: '2022-4-18 23：59 截止',
							tag: '可报名'
						},
						pic:'salon.svg',
						color:['#CEE0EF','#112C9A','#202969']
					}
				]
				
				
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
