<template>
	<view>
		<image src="../../../static/main/setting/background.png" style="width: 100%; height: 400rpx; opacity: 0.85;" />
		<!-- 页面总view -->
		<movable-area class="col-container" style="height: 100%;position: absolute; top:0rpx;">
			<!-- 除了背景图和底部按钮之外的所有部分,使用flex布局 -->
			<movable-view out-of-bounds direction="vertical" y="150rpx" class="main-view">
				<!-- 放置头像和身份信息tag的view -->
				<view class="row-container" style="padding:30rpx;margin-top: -20rpx;align-items: flex-end; ">
					<image class="avatar" :src="avatarurl"></image>
					<!-- 身份信息 -->
					<view class="identity-container">
						<!-- 昵称 -->
						<text class="nickname">{{nickname}}</text>
						<!-- 权限tag -->
						<view style="display: flex;">
							<view v-for="(item, index) in authorities" :key="index" :style="{background:item[1]}" class="authority-text">{{item[0]}}</view>
						</view>
						<!-- 用户id -->
						<view style="font:500 32rpx/40rpx sans-serif;">ID:{{id}}</view>
					</view>
				</view>
				<!-- 账号绑定 -->
				<weiyang-button class="unauthorizedinfo-container" bgcolor="#FFD5D5" hovercolor="#ffc4c4">
					<view class="unauthorizedinfo-container row-container">
						<image style="width: 75rpx; height: 75rpx;" src="../../../static/common/warning.svg" />
						<text class="warning-text">账号未绑定，点击此处进行绑定</text>
						<image style="width: 15rpx;margin-top: 6rpx;margin-left: 15rpx;"
							src="../../../static/main/setting/Arrow.svg" />
					</view>
				</weiyang-button>
				<!-- 操作按钮的容器 -->
				<view class="operations-container">
					<weiyang-button class="operation" style="margin-left: 15rpx;" bgcolor="transparent"
						hovercolor="#c8c8c8" :hasShadow="true">
						<view class="operation col-container">
							<image class="operation-icon" src="../../../static/main/setting/option_feedback.svg" />
							<text class="operation-text">反馈&建议</text>
						</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
					<weiyang-button class="operation" style="margin-left: 15rpx;" bgcolor="transparent"
						hovercolor="#c8c8c8">
						<view class="operation col-container">
							<image class="operation-icon" src="../../../static/main/setting/option_scan.svg" />
							<text class="operation-text">扫码登录</text>
						</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
				</view>
			</movable-view>
			<!-- 底部按钮及版本号 -->
			<view class="col-container" style="position: absolute;bottom: 0;">
				<weiyang-button style="z-index: 10;" bgcolor="#0087A9" hovercolor="#00657f">
					<view class="button-text">登录</view>
				</weiyang-button>
				<view class="col-container" style="font:300 20rpx sans-serif;margin: 17rpx;">
					Version: {{version}}
				</view>
			</view>
		</movable-area>
		<!-- 背景图片 -->
		<weiyang-background></weiyang-background>
	</view>
</template>

<script>
	const app = getApp()
	export default {
		data() {
			return {
				login:false,
				nickname: '未小羊',
				avatarurl:'../../../static/main/setting/avatar.png',
				id: 0,
				version: "2.0.0",
			}
		},
		computed:{
			authorities() {
				if(this.login) {
					let list=[['学生','#0087A9'],['教务','#008C0E'],['从游坊管理员','#6C3974'],['预约管理员','#0092A6'],['小程序管理员','#EF5DA8']]
					let ans=[]
					// 根据具体逻辑给ans增加项目
					return ans
				} else{
					return [['游客','black']]
				}
			}
		},
		methods: {
			logOut(e){
				console.log(e)
			},
			logIn(e){
				console.log(e)
			}
		},
		onLoad() {
			if(app.globalData.login){
				this.id=app.globalData.profile.id
				this.nickname=app.globalData.profile.name
			} else{
				
			}
		},
	}
</script>

<style>
	.main-view {
		display: flex;
		flex-direction: column;
		align-items: center;
	
		z-index: 10;
		width: 100%;
		height: calc(100% - 150rpx);

		background: linear-gradient(transparent 0%, transparent 196rpx, white 204rpx, white 600rpx, transparent 601rpx, transparent 100%);
	}

	/* 用户信息 */
	.identity-container {
		width: 400rpx;
		padding: 0 20rpx;

		display: flex;
		flex-direction: column;
		justify-content: flex-end;
	}
	/* 头像框 */
	.avatar {
		width: 300rpx;
		height: 300rpx;

		border: 10rpx solid #660874;
		border-radius: 50%;
		box-sizing: border-box;
		
		flex-shrink: 0;
	}
	/* 用户昵称 */
	.nickname {
		margin: 10rpx 0;
		font: 800 60rpx/70rpx sans-serif;
		text-shadow:
			2rpx 2rpx 0rpx #FFFFFF,
			-2rpx -2rpx 0rpx #FFFFFF,
			-2rpx 2rpx 0rpx #FFFFFF,
			2rpx -2rpx 0rpx #FFFFFF;
	}
	/* 权限文字的样式 */
	.authority-text {
		margin: 10rpx 5rpx;
		padding: 5rpx 10rpx;
		border-radius: 15rpx;
		color: #FFFFFF;
		font: 900 30rpx sans-serif;
	}


	/* 未授权的红色警告 */
	.unauthorizedinfo-container {
		width: 690rpx;
		height: 120rpx;
	}
	.warning-text {
		margin-left: 23rpx;

		color: #FF2727;
		font: bold 36rpx/42rpx sans-serif;
	}


	/* 更多选项 */
	.operations-container {
		width: 690rpx;
		height: 230rpx;
		margin-top: 20rpx;

		background: #DCDCDC;
		border-radius: 30rpx;

		display: flex;
		align-items: center;
	}
	.operation {
		width: 200rpx;
		height: 200rpx;
	}
	.dividing-lines {
		width: 0rpx;
		height: 180rpx;
		border: 1rpx solid #CCCCCC;
		margin-left: 15rpx;
	}
	.operation-icon {
		width: 150rpx;
		height: 150rpx;
	}
	.operation-text {
		font: 30rpx/35rpx sans-serif;
	}


	/* （退出）登录按钮样式 */
	.button-text {
		width: 690rpx;
		height: 120rpx;

		font: 900 36rpx/120rpx sans-serif;

		text-justify: kashida;
		color: #FFFFFF;
	}
</style>
