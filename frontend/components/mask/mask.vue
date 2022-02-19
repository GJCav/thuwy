<template>
	<view class="mask">
		<view class="mask-background"></view>
	</view>
</template>

<script>
	export default {
		name:"mask",
		data() {
			return {
				
			};
		}
	}
</script>

<style scoped>
	.mask {
		position: fixed;
		top: 0rpx;
		bottom: 0rpx;
		display: flex;
		width: 750rpx;
		height: 1500rpx;
	}
	
	.mask-background {
		width: 100%;
		height: 100%;
		z-index: 999;
		
		background-color: rgba(0, 0, 0, 1);
	}
</style>
