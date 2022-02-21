<template>
	<view class="weiyang-section">
		<view class="header">
			<view class="decoration" :style="{'--color':color}"></view>
			<view class="content">
				<text class="title">{{title}}</text>
				<text v-if="subtitle" class="sub">{{subtitle}}</text>
			</view>
		</view>
		<slot/>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-section',
		props: {
			title: {
				type: String,
				default: '我是标题'
			},
			subtitle: {
				type: String,
				default: ''
			},
			color: {
				type: String,
				default: '#0087A9'
			},
		},
		data() {
			return {}
		},
	}
</script>

<style scoped>
	.weiyang-section {
		width: 750rpx;
		background-color: #FFFFFF;
	}

	.header {
		display: flex;
		flex-direction: row;
		align-items: center;
		padding: 24rpx 20rpx;
		font-weight: bold;
	}

	.decoration {
		width: 10rpx;
		height: 36rpx;
		margin-right: 20rpx;
		border-radius: 20rpx;
		background-color: var(--color);
	}

	.content {
		display: flex;
		flex-direction: column;
	}

	.title {
		font-size: 36rpx;
		color: #333333;
	}

	.sub {
		font-size: 25rpx;
		font-weight: normal;
		color: #999999;
		line-height: 36rpx;
	}
</style>
