<template>
	<view>
		<weiyang-background></weiyang-background>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {

		}
	}
</script>

<style>
	/* 弹性容器 */
	.container { 
		display: flex;
		width: 100%;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
	}
</style>
