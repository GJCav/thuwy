<template>
	<view class="container">
		<view v-for="item in sample" :key="item">
			<weiyang-card :pattern="item">{{'卡片角标'}}</weiyang-card>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				sample:[11,12,13,21,22,31,32,33,34]	// 所用卡片样式一览
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
