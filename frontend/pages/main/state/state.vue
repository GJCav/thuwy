<template>
	<view class="col-container">
		<weiyang-section subtitle="我是副标题">
			<weiyang-forms></weiyang-forms>
		</weiyang-section>
		<view v-for="item in sample" :key="item">
			<weiyang-card :pattern="item">{{'卡片角标'}}</weiyang-card>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				value:'',
				sample:[11,12,13,21,22,31,32,33,34]	// 所用卡片样式一览
			}
		},
		methods: {
			
		}
	}
</script>

<style>
 uni-easyinput{
	 background-color: #000000;
 }
</style>
