<template>
	<view class="content">
		<!-- 上层 -->
		<view class="top-layer">
			<!-- 滑动窗口 -->
			<view class="swiper-with-indicator-dots">
				<swiper class="swiper" @change="swiperChange">
					<swiper-item v-for="(item,index) in list" :key="index">
						<image :src="item.src" class="swiper-item-image"></image>
						<view class="swiper-item-decoration"></view>
						<text class="swiper-item-text">{{item.text}}</text>
					</swiper-item>
				</swiper>
				<view class="indicator-dots-container">
					<view :class="current==index?'indicator-dot-active':'indicator-dot'" v-for="(item,index) in list" :key="index"></view>
				</view>
			</view>
			<!-- 功能按钮 -->
			<view class="buttons-container">
				<view class="button">
					<image src="./icon_ReserveServ.svg" class="button-icon"></image>
					<text class="button-text">预约服务</text>
				</view>
				<view class="button">
					<image src="./icon_EduAdminQA.svg" class="button-icon"></image>
					<text class="button-text">教务答疑</text>
				</view>
				<view class="button">
					<image src="./icon_CongyouSeminar.svg" class="button-icon"></image>
					<text class="button-text">从游坊</text>
				</view>
			</view>
		</view>
		<view>
			<weiyang-background></weiyang-background>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				list: [
					{
						src: '/static/AED.jpg',
						text: 'AED位置&使用方法演示'
					},
					{
						src: '/static/AED.jpg',
						text: 'AED位置&使用方法演示'
					},
					{
						src: '/static/AED.jpg',
						text: 'AED位置&使用方法演示'
					}
				],
				current: 0
			};
		},
		onLoad() {

		},
		methods: {
			swiperChange(event) {
				this.current = event.detail.current;
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	
	/* 背景层 */
	.background-layer {
		z-index: -10;
	}
	
	/* 背景未央标志 */
	.background-image {
		width: 700rpx;
		height: 637.76rpx;
		
		position: absolute;
		left: 150rpx;
		top: 725rpx;
		
		opacity: 0.6;
	}
	
	/* 上层 */
	.top-layer {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 1;
	}
	
	/* 主页顶部滑动窗口与指示点容器 */
	.swiper-with-indicator-dots {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin-top: 20rpx;
		margin-bottom: 80rpx;
	}
	
	/* 主页顶部滑动窗口 */
	.swiper {
		width: 600rpx;
		height: 400rpx;
		margin-bottom: 15rpx;
	}
	
	/* 指示点容器 */
	.indicator-dots-container {
		width: 500rpx;
		height: 20rpx;
		
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	/* 指示点 */
	.indicator-dot {
		width: 10rpx;
		height: 10rpx;
		
		margin-left: 5rpx;
		margin-right: 5rpx;
		
		border-radius: 50%;
		background-color: #C0E1EA;
	}
	
	/* 当前指示点 */
	.indicator-dot-active {
		width: 10rpx;
		height: 10rpx;
		
		margin-left: 5rpx;
		margin-right: 5rpx;
		
		border-radius: 50%;
		background-color: #0087A9;
	}
	
	/* 主页顶部滑动窗口内容图片*/
	.swiper-item-image {
		height: 100%;
		width: 100%;
		
		position: absolute;
		
		border-radius: 25rpx;
	}
	
	/* 主页顶部滑动窗口渐变装饰 */
	.swiper-item-decoration {
		width: 600rpx;
		height: 100rpx;
		
		position: absolute;
		left: 0rpx;
		top: 300rpx;
		
		background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.4) 100%, rgba(0, 0, 0, 0.4) 100%);
		border-radius: 25rpx;
	}
	
	/* 主页顶部滑动窗口文字 */
	.swiper-item-text {
		height: 60rpx;
		
		position: absolute;
		left: 25rpx;
		bottom: 15rpx;
		
		font-style: normal;
		font-weight: 900;
		font-size: 40rpx;
		line-height: 60rpx;
		color: #FFFFFF;
	}
	
	/* 主页按钮容器 */
	.buttons-container {
		width: 600rpx;
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: space-bwtween;
	}
	
	/* 主页按钮 */
	.button {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-left: 25rpx;
		margin-right: 25rpx;
		margin-bottom: 29rpx;
	}
	
	/* 主页按钮文本 */
	.button-text {
		height: 54rpx;
		margin-top: 17rpx;
		
		text-align: center;
		font-style: normal;
		font-weight: 900;
		font-size: 36rpx;
		line-height: 54rpx;
		color: #000000;
		text-shadow: #FFFFFF 2rpx 0 0, #FFFFFF -2rpx 0 0, #FFFFFF 0 2rpx 0, #FFFFFF 0 -2rpx 0;
		
	}
	
	/* 主页按钮图标 */
	.button-icon {
		max-width: 250rpx;
		max-height: 250rpx;
	}
</style>
