<template>
	<view>
		<!-- carousel窗口 -->
		<swiper class="col-container" @change="swiperChange">
			<swiper-item v-for="(item,index) in carousel_list" :key="index">
				<image :src="item.src" class="swiper-item-image"></image>
				<view class="swiper-item-decoration"></view>
				<text class="swiper-item-text">{{item.text}}</text>
			</swiper-item>
		</swiper>
		<view class="row-container">
			<view :class="current==index?'indicator-dot-active':'indicator-dot'" v-for="(item,index) in carousel_list"
				:key="index"></view>
		</view>
		<!-- 功能按钮 -->
		<view class="row-container" style="flex-wrap: wrap;justify-content: space-between;padding:50rpx 10%;">
			<view class="col-container" style="width: 270rpx;" v-for="(item,index) in button_list" :key="index">
				<image :src="item.src" class="button-icon"></image>
				<text class="button-text">{{item.text}}</text>
			</view>
		</view>
		<!-- 背景图片 -->
		<weiyang-background></weiyang-background>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				current: 0, // carousel索引
				carousel_list: [{ // carousel信息
					src: '/static/AED.jpg',
					text: 'AED位置&使用方法演示'
				}, {
					src: '/static/AED.jpg',
					text: 'AED位置&使用方法演示'
				}, {
					src: '/static/AED.jpg',
					text: 'AED位置&使用方法演示'
				}],
				button_list: [{
					src: '/static/main/index/ReserveServe.svg',
					text: '预约服务'
				}, {
					src: '/static/main/index/EduAdminQA.svg',
					text: '教务答疑'
				}, {
					src: '/static/main/index/CongyouSeminar.svg',
					text: '从游坊'
				}]
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

<style lang="scss">
	/* 主页顶部滑动窗口 */
	swiper {
		height: 400rpx;
		margin: 18rpx 0;
	}

	@mixin swiper-justify {
		width: 80%;
		position: absolute;
		left: 10%;
		bottom: 0;
	}

	swiper-item {

		/* 主页顶部滑动窗口内容装饰 */
		.swiper-item-decoration {
			@include swiper-justify;
			height: 100rpx;

			border-radius: 25rpx;
			background: linear-gradient(180deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.4));
		}

		/* 主页顶部滑动窗口内容图片*/
		.swiper-item-image {
			@include swiper-justify;
			height: 100%;
			border-radius: 25rpx;
		}

		/* 主页顶部滑动窗口文字 */
		.swiper-item-text {
			@include swiper-justify;
			padding: 15rpx 25rpx;

			font-weight: 900;
			font-size: 40rpx;
			color: #FFFFFF;
		}

	}


	/* 指示点 */
	.indicator-dot {
		width: 10rpx;
		height: 10rpx;

		margin: 0 5rpx;

		border-radius: 50%;
		background-color: #C0E1EA;
	}

	/* 当前指示点 */
	.indicator-dot-active {
		@extend .indicator-dot;
		background-color: #0087A9;
	}


	/* 主页按钮样式 */
	/* 主页按钮文本 */
	.button-text {
		height: 54rpx;
		margin: 17rpx 0 30rpx;

		text-align: center;
		font-style: normal;
		font-weight: 900;
		font-size: 36rpx;
		color: #000000;
		text-shadow: #FFFFFF 2rpx 2rpx 0, #FFFFFF -2rpx -2rpx 0;

	}

	/* 主页按钮图标 */
	.button-icon {
		max-width: 250rpx;
		max-height: 250rpx;
		padding: 10rpx;
		border-radius: 30rpx;
		background-color: #FFFFFF;
	}
</style>
