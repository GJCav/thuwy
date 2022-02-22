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
							<view v-for="(item, index) in authorities" :key="index" :style="{background:item[1]}"
								class="authority-text">{{item[0]}}</view>
						</view>
						<!-- 用户id -->
						<view style="font:500 32rpx/40rpx sans-serif;">ID:{{id}}</view>
					</view>
				</view>
				<!-- 账号绑定 -->
				<navigator url="../bind/bind" v-if="!hasBind">
					<weiyang-button class="unauthorizedinfo-container" bgcolor="#FFD5D5" hovercolor="#ffc4c4">
						<view class="row-container" style="height: 120rpx;">
							<image style="width: 75rpx; height: 75rpx;" src="../../../static/common/warning.svg" />
							<text class="warning-text">账号未绑定，点击此处进行绑定</text>
							<image style="width:15rpx;margin-left:15rpx;"
								src="../../../static/main/setting/Arrow.svg" />
						</view>
					</weiyang-button>
				</navigator>
				<!-- 操作按钮的容器 -->
				<view class="operations-container">
					<weiyang-button bgcolor="transparent" hovercolor="#c8c8c8">
						<image class="operation-icon" src="../../../static/main/setting/option_feedback.svg" />
						<view class="operation-text">反馈&建议</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
					<weiyang-button bgcolor="transparent" hovercolor="#c8c8c8" @click="scanQR()">
						<image class="operation-icon" src="../../../static/main/setting/option_scan.svg" />
						<view class="operation-text">扫码登录</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
					<!-- 占位view -->
					<view style="width: 190rpx;"></view>
				</view>
			</movable-view>
		</movable-area>
		<!-- 底部按钮及版本号 -->
		<view class="col-container" style="z-index:100 ;position: absolute;bottom: 0;">
			<weiyang-button bgcolor="#0087A9" hovercolor="#00657f" @click="onClickLog">
				<view class="button-text">{{loginButtonText}}</view>
			</weiyang-button>
			<view class="col-container" style="font:300 20rpx sans-serif;margin: 17rpx;">
				Version: {{version}}
			</view>
		</view>
		<!-- 背景图片 -->
		<weiyang-background></weiyang-background>
	</view>
</template>

<script>
	const app = getApp()
	export default {
		data() {
			return {
				nickname: '未小羊',
				avatarurl: '../../../static/main/setting/avatar.png',
				id: 0,
				version: "2.0.0",
				loginButtonText: "登录",
				hasBind: false,
			}
		},
		computed: {
			authorities() {
				if (this.login) {
					let list = [
						['学生', '#0087A9'],
						['教务', '#008C0E'],
						['从游坊管理员', '#6C3974'],
						['预约管理员', '#0092A6'],
						['小程序管理员', '#EF5DA8']
					]
					let ans = []
					// 根据具体逻辑给ans增加项目
					if (app.globalData.profile.clazz === "未央教务") {
						ans.append(list[1]);
					}
					else {
						ans.append(list[0]);
					}
					let isAdmin = app.globalData.profile.all-privileges.indexOf('admin'); //借用管理员
					let isCongyou_admin = app.globalData.profile.all-privileges.indexOf('congyou');//从游管理员
					if (isAdmin && isCongyou_admin) {
						//小程序管理员
						ans.append(list[4]);
					} else {
						if (isAdmin) {
							//借用管理员
							ans.append(list[3]);
						}
						if (isCongyou_admin) {
							//从游管理员
							ans.append(list[2]);
						}
					}
					return ans
				} else {
					return [
						['游客', 'black']
					]
				}
			}
		},
		onShow() {
			console.log("登录: " + app.globalData.login);
			if (app.globalData.login) {
				this.id = app.globalData.profile.id || 'NaN';
				this.nickname = app.globalData.profile.name || '未绑定';
				this.loginButtonText = "退出登录";
			} else {
				this.loginButtonText = "登录";
			}
			this.hasBind = (app.globalData.profile.id!=null);
			console.log("绑定: " + this.hasBind);
		},

		methods: {
			logOut() {
				// uni.clearStorage();
				app.globalData.login = false;
				app.globalData.profile = null;
				app.globalData.logincode = null;
				uni.reLaunch({
					url: "../index/index",
				});
				uni.showToast({
					title: '登出成功',
					icon: 'success',
					duration: 1500,
					mask: true
				});
			},
			logIn() {
				let that = app;
				uni.login()
				.then(res => { // 获取openID
					that.globalData.logincode = res.code;
					// console.log(that.globalData.logincode);
					return uni.request({ // 发送 res.code 到后台换取 openId, sessionKey, unionId
						url: that.globalData.url.backend + '/login/',
						method: 'POST',
						data: {
							code: res.code
						}
					})
				})
				.then(res => { // 储存openID并请求用户信息
					if (res.data.code == 0) {
						uni.setStorage({ // 将得到的openid存储到缓存里面方便后面调用
							key: "cookie",
							data: res.cookies[0]
						})
						// console.log(res.cookies);
						// console.log("step two finished");
						return uni.request({
							url: that.globalData.url.backend + '/profile/',
							method: 'GET',
							header: {
								'content-type': 'application/json; charset=utf-8',
								'cookie': res.cookies[0]
							},
						})
					} else {
						throw res
					}
				})
				.then(res => { // 储存用户信息
					if (res.data.code == 0) {
						that.globalData.profile = {
							name: res.data.name,
							class: res.data.clazz,
							id: res.data['school-id'],
							privileges: res.data.privileges
						}
						console.log(that.globalData.profile)
						that.globalData.login = true;
						// console.log(that.globalData.login);
						uni.showToast({
							title: '登录成功',
							icon: 'success',
							duration: 1500,
							mask: true
						});
					} else {
						throw res
					}
				})
				.catch(err => {
					console.log(err)
				});
				uni.reLaunch({
					url: "../index/index",
				});
			},
			
			onClickLog(e) {
				//点击登录或者退出登录按钮
				if (app.globalData.login) {
					this.logOut();
				}
				else {
					this.logIn();
				}
			},
			scanQR() {
				// ISSUE: 无法拉取信息
				uni.scanCode({
					onlyFromCamera: true,
					scanType: ['qrCode'],
					success: res => {
						//TODO: 如果没有登录，直接不让用户点扫码这个按钮
						uni.showModal({
							title: '登录网页端',
							content: '是否确认登录？',
							success(modelRes) {
								if (modelRes.confirm) {
									uni.request({
										url: `${app.globalData.url.backend}/weblogin`,
										method: 'POST',
										dataType: 'json',
										data: {
											requestedId: res.result,
											redential: app.globalData.logincode,
										},
										success: ({ data }) => {
											if (data.code === 0) {
												uni.showToast({
													title: '登录成功',
													icon: 'success',
													duration: 1500,
													mask: true
												});
											} else {
												uni.showToast({
													title: data.msg,
													icon: 'error',
													duration: 1500,
													mask: true
												});
											}
										},
										fail: (res) => {
											console.log('扫码登录失败错误：');
											console.log(res);
											uni.showToast({
												title: '拉取信息失败',
												icon: 'error',
												duration: 1500,
												mask: true
											});
										}
									});
								}
							}
						})
					}
				});
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
		width: 710rpx;
		height: 140rpx;
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
		justify-content: space-evenly;
	}

	.dividing-lines {
		width: 0rpx;
		height: 180rpx;
		border: 1rpx solid #CCCCCC;
	}

	.operation-icon {
		width: 150rpx;
		height: 150rpx;
	}

	.operation-text {
		color: #000000;
		font: 30rpx sans-serif;
	}


	/* （退出）登录按钮样式 */
	.button-text {
		width: 610rpx;
		margin: 20rpx;

		text-justify: kashida;
		font: 900 36rpx sans-serif;
	}
</style>
