<template>
	<view>
		<image class="weiyang-background" :style="distance" mode="widthFix" src="@/static/components/weiyang-background/weiyang.svg"></image>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-background',
		props:{
			distance:{
				default:{bottom: '-15rpx'},
			}
		},
		data() {
			return {}
		},
	}
</script>

<style scoped>
	.weiyang-background {
		position: fixed;
		width: 600rpx;
		right: 0rpx;
		z-index: -15;
	}
</style>
