<template>
	<view @click="NavigatePage()">
		<view class="weiyang-card" :style="{color:color[1],'background-color':color[0]}">
			<view class="flex-line" style="align-items: flex-start;">
				<view class="title">{{text.title}}</view>
				<view class="corner">
					<slot />
				</view>
			</view>
			<view class="theme">{{text.theme}}</view>
			<view class="content" :style="{color:color[2]}">{{text.content}}</view>
			<view class="flex-line" style="align-items: flex-end;">
				<view class="info">{{text.info}}</view>
				<view class="tag" :style="{'background-color':color[1]}">{{text.tag}}</view>
			</view>
			<image class="weiyang-card-background" mode="widthFix" :src="picurl"></image>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-card',
		data() {
			return {
				colordata: [
					[ // 物品预约
						['#DAF3ED', '#45C5A6', '#37806F'],
						['#E5EFEC', '#607870', '#323E3A'],
						['#FDF1EE', '#EB3341', '#380A0A'],
					],
					[ // 教务答疑
						['#CEE0EF', '#112C9A', '#202969'],
						['#D6DDE3', '#202969', '#171D4D'],
					],
					[ // 从游坊
						['#D2CEF0', '#5800A6', '#440080'],
						['#D0CFDD', '#4B2D74', '#311E4D'],
						['#FDF1EE', '#EB3341', '#380A0A'],
						["#F3F3F3", "#CCCCCC", "#999999"],
					]
				]
			}
		},
		props: {
			text: { // 卡片文本
				type: Object,
				default () {
					return {
						title: '卡片标题',
						theme: '卡片主题',
						content: '卡片正文',
						info: '卡片信息',
						tag: '卡片标签'
					}
				}
			},
			pattern: { // 卡片样式
				type: Number,
				default: 11
			},
			url: { // 跳转绝对路径,可带参数
				type: String,
				required: true
			}
		},
		computed: {
			picurl() {
				return '../../static/components/weiyang-card/' + String(this.pattern) + '.svg'
			},
			color() {
				return this.colordata[parseInt(this.pattern / 10) - 1][this.pattern % 10 - 1]
			}
		},
		methods: {
			NavigatePage() {
				console.log(this.url)
				uni.navigateTo({
					url: this.url
				})
			}
		},
	}
</script>

<style scoped>
	/* 整体卡片排版 */
	.weiyang-card {
		display: flex;
		flex-direction: column;

		position: relative;
		z-index: -2;
		overflow: hidden;

		width: 650rpx;
		padding: 20rpx;
		margin: 20rpx 0 0 0;
		border-radius: 30rpx;
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
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		font: bold 36rpx sans-serif;
	}

	.tag {
		padding: 3rpx 10rpx;
		border-radius: 10rpx;

		color: #FFFFFF;
		font: 900 40rpx sans-serif
	}

	/* 背景图片 */
	.weiyang-card-background {
		width: 300rpx;
		position: absolute;
		right: 0;
		bottom: -50rpx;
		z-index: -1;
	}
</style>
