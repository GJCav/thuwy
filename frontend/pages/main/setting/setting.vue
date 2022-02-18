<template>
	<view>
		<!-- <view class="img-container"
			style="background-image: linear-gradient(rgba(255,255,255,0.2) 95%, rgba(255,255,255,1)), url(static/setting/background_pic.png)">
		</view> -->
		<image
			src="../../../static/main/setting/background.png"
			style="width: 100%; height: 400rpx; opacity: 0.85;"
		/>
		<image
			src="../../../static/main/setting/background.png"
			style="margin-top: -10rpx;width: 100%; height: 100rpx; opacity: 0.85; object-fit:cover;transform: rotateX(180deg);"
		/>
		<movable-area
			style="position: absolute; top:0rpx; width: 100%; height: calc(100%); display: flex; flex-direction: column;">
			<!-- 页面总view -->
			<movable-view out-of-bounds direction="vertical" y="150rpx"
				style="height: calc(100% - 150rpx);" class="main-view">
				<!-- 除了背景图和底部按钮之外的所有部分,使用flex布局 -->
				<view style="display: flex;flex-flow: row wrap;align-content: flex-start;">
					<!-- 放置头像和身份信息tag的view -->
					<image class="avatar" src="../../../static/main/setting/avatar.png"></image>
					<view class="identity-container">
						<!-- 身份信息 -->
						<text class="nickname"><open-data type="userNickName"></open-data></text>
						<view class="authorities-view">
							<!-- 权限和id，flex布局 -->
							<view v-for="(item, ind) in authorities" :key="item.index" class="authority-container"
								:class="item.class">
								<!-- 权限tag -->
								<text class="authority-text">{{item.title}}</text>
							</view>
							<view>
								<!-- id -->
								<text class="id">ID:{{id}}</text>
							</view>
						</view>
					</view>
				</view>
				<weiyang-button class="unauthorizedinfo-container" style="margin-left: 30rpx;" bgcolor="#FFD5D5" hovercolor="#ffc4c4">
					<!-- 账号绑定 -->
					<view class="unauthorizedinfo-container flex-row">
						<image
							style="width: 75rpx; height: 75rpx;"
							src="../../../static/common/warning.svg" 
						/>
						<text class="warning-text">账号未绑定，点击此处进行绑定</text>
						<image
							style="width: 15rpx;margin-top: 6rpx;margin-left: 15rpx;"
							src="../../../static/main/setting/Arrow.svg" 
						/>
					</view>
				</weiyang-button>
				<view class="operations-container">
					<!-- 操作按钮的容器 -->
					<weiyang-button class="operation" style="margin-left: 15rpx;" bgcolor="transparent" hovercolor="#c8c8c8" hasShadow="true">
						<view class="operation flex-column">
							<image 
								class="operation-icon"
								src="../../../static/main/setting/option_feedback.svg"
							/>
							<text class="operation-text">反馈&建议</text>
						</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
					<weiyang-button class="operation" style="margin-left: 15rpx;" bgcolor="transparent" hovercolor="#c8c8c8">
						<view class="operation flex-column">
							<image
								class="operation-icon"
								src="../../../static/main/setting/option_scan.svg"
							/>
							<text class="operation-text">扫码登录</text>
						</view>
					</weiyang-button>
					<view class="dividing-lines"></view>
				</view>
			</movable-view>
			<view style="flex-grow: 1;"></view>
			<weiyang-button style="z-index: 100;" class="log-off flex-row" bgcolor="#0087A9" hovercolor="#00657f">
				<view class="button-text">退出登录</view>
			</weiyang-button>
			<view style="margin-left: 322rpx; margin-top: 0rpx">
				<text
					style="font-family: Roboto;font-style: normal;font-weight: 300;font-size: 18rpx;color: #000000;">
					Version: {{version}}
				</text>
			</view>
		</movable-area>
		<weiyang-background></weiyang-background>
	</view>
</template>

<script>
	const app=getApp()
	export default {
		data() {
			return {
				nickname: '未小羊',
				authorities: [{
						title: '学生',
						index: 0,
						class: "student-auth"
					},
					// {title: '教务', index: 1, class:"teacher-auth"},
					// {title: '从游坊管理员', index: 2, class:"cyf-admin-auth"},
					// {title: '借用管理员', index: 3, class:"lending-admin-auth"},
					{
						title: '小程序管理员',
						index: 4,
						class: "mp-admin-auth"
					},
				],
				id: 2020999999,
				version: "2.0.0",
				windowHeight: 0,
				windowWidth: 0,
				widowHeightinRpx: 0,
				tapPositionX: "-100rpx",
				tapPositionY: "-100rpx",
				gradient_radius: "20%",
				isFocusOff: true
			}
		},
		onLoad() {
			let that = this;
			uni.getUserProfile({
			    desc: '展示用户信息',
				success(res) {
					console.log(res)
				},
				fail(res){
					console.log(res)
				}
			})
			uni.getSystemInfo({
				success(res) {
					that.windowHeight = res.windowHeight;
					that.windowWidth = res.windowWidth;
					that.widowHeightinRpx = res.windowHeight / res.windowWidth * 750;
				}
			});

		},
		methods: {
			onTouchStart(e) {
				this.gradient_radius = "20%";
				this.isFocusOff = false;
				// console.log(e);
				this.tapPositionX = (e.touches[0].pageX - e.target.offsetLeft) / this.windowWidth * 750 + 'rpx';
				this.tapPositionY = (e.touches[0].pageY - e.target.offsetTop) / this.windowWidth * 750 + 'rpx';
				// for (var t = Date.now(); Date.now() - t <= 100;)
				// 	console.log();
				// this.isFocusOff = true;
			},
			sleep(d) {
				for (var t = Date.now(); Date.now() - t <= d;);
			},
			onTouchEnd(e) {
				this.isFocusOff = true;
			}
		},
	}
</script>

<style>
	.flex-row {
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.flex-column {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.img-top {
		/* 背景图片 */
		z-index: -10;
		width: 750rpx;
		height: 400rpx;
		opacity: 0;
	}

	.img-container {
		height: 400rpx;
		width: 750rpx;
		background: no-repeat center top / 100% 100%;
		overflow: hidden;
		opacity: 0.85;
	}

	.main-view {
		/* z-index: 10; */
		z-index: 10;
		width: 100%;
		

		background: linear-gradient(transparent 0%, transparent 196rpx, white 204rpx, white 600rpx, transparent 601rpx, transparent 100%);

		display: flex;
		flex-flow: column nowrap;
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
			2rpx 2rpx 0rpx #FFFFFF,
			-2rpx -2rpx 0rpx #FFFFFF,
			-2rpx 2rpx 0rpx #FFFFFF,
			2rpx -2rpx 0rpx #FFFFFF;
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
		overflow: hidden;
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
		font-family: Roboto;
		font-style: normal;
		font-weight: normal;
		font-size: 30rpx;
		line-height: 35rpx;
	}

	.button-text {
		width: 690rpx;
		height: 120rpx;
		font-family: Roboto;
		font-style: normal;
		font-weight: 900;
		font-size: 36rpx;
		line-height: 120rpx;
		text-align: center;
		text-justify: kashida;
		color: #FFFFFF;
	}
	.log-off {
		width: 690rpx;
		height: 120rpx;
		margin-left: 30rpx;
	}
	
	
</style>
