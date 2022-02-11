<template>
	<view>
		<image class="weiyang-background" src="../../static/weiyang.svg"></image>
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

<style>
	.weiyang-background {
		position: fixed;
		bottom: -10rpx;
		left: 150rpx;
		z-index: -20;
	}
</style>
