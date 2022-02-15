<template>
	<view>
		<image class="weiyang-background" mode="widthFix" src="@/static/components/weiyang-background/weiyang.svg"></image>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-background',
		data() {
			return {}
		},
	}
</script>

<style scoped>
	.weiyang-background {
		position: fixed;
		width: 600rpx;
		bottom: -15rpx;
		right: 0rpx;
		z-index: -15;
	}
</style>
