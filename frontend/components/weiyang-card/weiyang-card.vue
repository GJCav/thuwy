<template>
	<view class="weiyang-card" :style="normal_color">
		<view class="flex-line" style="align-items: flex-start;">
			<view class="title">{{text.title}}</view>
			<view class="corner">{{text.corner}}</view>
		</view>
		<view class="theme">{{text.theme}}</view>
		<view class="content">{{text.content}}</view>
		<view class="flex-line" style="align-items: flex-end;">
			<view class="info">{{text.info}}</view>
			<view class="tag">{{text.tag}}</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-card',
		props: {
			text: { // 卡片文本
				type: Object,
				default () {
					return {
						title: '卡片标题',
						corner: '卡片角标',
						theme: '卡片主题',
						content: '卡片正文',
						info: '卡片信息',
						tag: '卡片标签'
					}
				}
			},
			color: { // 卡片色调
				type: Array,
				default:['#F3F3F3','#CCCCCC','#999999']
			},
			url: { // 跳转绝对路径
				type: String,
				default: '/pages/main/index/index'
			}
		},
		computed:{
			light_color(){
				return{
					color:this.color[0]
				}
			},
			normal_color(){
				return{
					color:this.color[1]
				}
			},
			dark_color(){
				return{
					color:this.color[2]
				}
			}
		}
	}
</script>

<style>
	/* 整体卡片排版 */
	.weiyang-card {
		display: flex;
		flex-direction: column;

		width: 650rpx;
		padding: 20rpx;
		margin: 20rpx 0 0 0;
		border-radius: 30rpx;
		border: 2rpx solid #000000;
	}

	/* 横向弹性框 */
	.flex-line {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	/* 卡片各项信息细节 */
	.title {
		height: 70rpx;
		font: 900 54rpx sans-serif;
	}

	.corner {
		font: medium 25rpx sans-serif;
	}

	.theme,
	.info {
		font: bold 30rpx sans-serif;
	}

	.content {
		padding: 30rpx 0;
		font: bold 36rpx sans-serif;
	}

	.tag {
		padding: 3rpx 10rpx;
		border-radius: 10rpx;
		background-color: #000000;

		color: #FFFFFF;
		font: 900 40rpx sans-serif
	}
</style>
