<template>
	<view class="bground">
		<view style="display: flex; flex-direction: column" :style="{ height: windowHeight + 'px' }"> <!-- 页面总view -->
			<image class="img-top" src="../../../static/setting/background_pic.png"></image>
			<view class="main-view"> <!-- 除了背景图之外的所有部分,使用flex布局 -->
				<image class="avatar" src="../../../static/setting/avatar_default.png"></image>
				<view class="identity-container"> <!-- 身份信息 -->
					<text class="nickname">{{nickname}}</text>
					<view class="authorities-view"> <!-- 权限和id，flex布局 -->
						<view v-for="(item, ind) in authorities" :key="item.index" class="authority-container" :class="item.class"> <!-- 权限tag -->
							<text class="authority-text">{{item.title}}</text>
						</view>
						<view> <!-- id -->
							<text class="id">ID:{{id}}</text>
						</view>
					</view>
				</view>
				<view class="unauthorizedinfo-container"> <!-- 账号绑定 -->
					<image style="width: 75rpx; height: 75rpx;" src="../../../static/setting/Warning.svg"></image>
					<text class="warning-text">账号未绑定，点击此处进行绑定</text>
					<image style="width: 15rpx;margin-top: 6rpx;margin-left: 15rpx;" src="../../../static/setting/Arrow.svg"></image>
				</view>
				<view class="operations-container"> <!-- 操作按钮的容器 -->
					<view class="operations">
						<image class="operation-icon" src="../../../static/setting/feedback.svg"></image>
						<text class="operation-text">反馈&建议</text>
					</view>
					<view class="dividing-lines"></view>
					<view class="operations">
						<image class="operation-icon" src="../../../static/setting/scan_to_sign_in.svg"></image>
						<text class="operation-text">扫码登录</text>
					</view>
					<view class="dividing-lines"></view>
				</view>
			
				
			</view>
			<view style="flex-grow: 1;"></view>
			<button class="buttons"><text style="font: 36rpx 900 Roboto; color: #FFFFFF;line-height: 42rpx;">退出登录</text></button>
			<view style="margin-left: 322rpx; margin-top: 0rpx">
				<text style="font-family: Roboto;font-style: normal;font-weight: 300;font-size: 18rpx;color: #000000;">Version: {{version}}</text>
			</view>
		</view>
		<image class="dandelion" src="../../../static/setting/dandelion.svg"></image>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				nickname: '未小羊',
				authorities: [
					{title: '学生', index: 0, class:"student-auth"},
					// {title: '教务', index: 1, class:"teacher-auth"},
					// {title: '从游坊管理员', index: 2, class:"cyf-admin-auth"},
					// {title: '借用管理员', index: 3, class:"lending-admin-auth"},
					{title: '小程序管理员', index: 4, class:"mp-admin-auth"},
				],
				id: 2020999999,
				version: "2.0.0",
				windowHeight: 0
			}
		},
		onLoad() {
			let that = this;
			uni.getSystemInfo({
				success(res) {
					that.windowHeight = res.windowHeight;
				}
			})
		},
		methods: {
			
		}
	}
</script>

<style>
	.img-top {
		/* 背景图片 */
		/* position: absolute; */
		width: 750rpx;
		height: 400rpx;
	}
	
	.main-view {
		margin-top: -200rpx;
		z-index: 100;
		
		display: flex;
		flex-flow: row wrap;
		align-content: flex-start;
		flex-grow: 0;
		flex-shrink: 0;
	}
	
	.identity-container {
		width: 375rpx;
		display: flex;
		flex-flow: column nowrap;
	}
	
	.avatar {
		/* 头像框 */
		width: 300rpx;
		height: 300rpx;
		
		margin-left: 30rpx;
		margin-top: 0rpx;
		margin-bottom: 10rpx;
		
		border: 10rpx solid #660874;
		border-radius: 50%;
		box-sizing: border-box;
	}
	.nickname {
		/* 用户昵称 */
		/* position: relative; */
		/* width: 180rpx; */
		/* height: 70rpx; */
		/* left: 355rpx;
		top: -70rpx; */
		margin-left: 25rpx;
		margin-top: 125rpx;
		
		font-family: Roboto;
		font-style: normal;
		font-weight: 800;
		font-size: 60rpx;
		line-height: 70rpx;
		
		color: #000;
		text-shadow:
			2rpx 0rpx 0rpx #FFFFFF,
			-2rpx 0rpx 0rpx #FFFFFF,
			0rpx 2rpx 0rpx #FFFFFF,
			0rpx -2rpx 0rpx #FFFFFF;
	}
	.student-auth {
		/* 学生 */
		width: 80rpx;
		height: 40rpx;
		
		background: #0087A9;
	}
	.teacher-auth {
		/* 教务 */
		width: 80rpx;
		height: 40rpx;
		
		background: #008C0E;
	}
	.cyf-admin-auth {
		/* 从游坊管理员 */
		width: 200rpx;
		height: 40rpx;
		
		background: #6C3974;
	}
	.lending-admin-auth {
		/* 借用管理员 */
		width: 170rpx;
		height: 40rpx;
		
		background: #0092A6;
	}
	.mp-admin-auth {
		/* 小程序管理员 */
		width: 200rpx;
		height: 40rpx;
		
		background: #EF5DA8;
	}
	.authorities-view {
		/* 所有权限标签的总体容器 */
		margin-left: 15rpx;
		margin-top: 15rpx;
		margin-bottom: 18rpx;
		
		width: 400rpx;
		/* height: 200rpx; */
		
		display: flex;
		flex-flow: row wrap;
		align-content: flex-start;
	}
	.authority-text {
		/* 权限文字的样式 */
		width: 180rpx;
		height: 35rpx;
		
		font-family: Roboto;
		font-style: normal;
		font-weight: 900;
		font-size: 30rpx;
		line-height: 35rpx;
		
		text-align: center;
		color: #FFFFFF;
	}
	.authority-container {
		/* 单个权限标签的样式 */
		margin: 5rpx 5rpx 5rpx 5rpx;
		
		border-radius: 15rpx;
		
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.id {
		width: 248rpx;
		height: 42rpx;
		margin-left: 10rpx;
		margin-top: 10rpx;
		
		font-family: Roboto;
		font-style: normal;
		font-weight: 500;
		font-size: 32rpx;
		line-height: 42rpx;
		
		color: #000;
	}
	
	.unauthorizedinfo-container {
		/* 未授权的红色警告 */
		width: 690rpx;
		height: 120rpx;
		
		margin-left: 30rpx;
		
		background: #FFD5D5;
		border-radius: 30rpx;
		
		display: flex;
		justify-content: center;
		align-items: center;
	}
	
	.warning-text {
		margin-left: 23rpx;
		
		font-family: Roboto;
		font-style: normal;
		font-weight: bold;
		font-size: 36rpx;
		line-height: 42rpx;
		
		color: #FF2727;
	}
	
	.operations-container {
		width: 690rpx;
		height: 230rpx;
		margin-left: 30rpx;
		margin-top: 20rpx;
		
		background: #DCDCDC;
		border-radius: 30rpx;
		
		display: flex;
		align-items: center;
	}
	.dividing-lines {
		width: 0rpx;
		height: 180rpx;		
		border: 1rpx solid #CCCCCC;
		margin-left: 40rpx;
	}
	.operations {
		width: 150rpx;
		margin-left: 40rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		/* flex-grow: 1; */
	}
	.operation-icon {
		width: 150rpx;
		height: 150rpx;
	}
	.operation-text {
		font-family: Roboto;
		font-style: normal;
		font-weight: normal;
		font-size: 30rpx;
		line-height: 35rpx;
	}
	.buttons {
		width: 690rpx;
		height: 120rpx;
		background: #0087A9;
		border-radius: 30rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.bground {
		opacity: 1;
	}
	.dandelion {
		z-index: -10;
		position: absolute;
		width: 700rpx;
		height: 637.76rpx;
		left: 150rpx;
		bottom: 0rpx;
		
		opacity: 0.6;
	}
</style>
