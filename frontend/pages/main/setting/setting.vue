<template>
	<view>
		<!-- 页面总view -->
		<image class="img_top" src="../../../static/setting/背景图片.png"></image>
		<view class="main_view">
			<!-- 除了背景图之外的所有部分 -->
			<view>
				<!-- 身份信息 -->
				<image class="avatar" src="../../../static/setting/avatar_default.png"></image>
				<text class="nickname">{{nickname}}</text>
				<view class="authorities_view">
					<!-- 权限和id，flex布局 -->
					<view v-for="(item, ind) in authorities" :key="item.index" class="authority_container" :class="item.class">
						<!-- 权限tag -->
						<text class="authority_text">{{item.title}}</text>
					</view>
					<view>
						<!-- id -->
						<text class="id">ID:{{id}}</text>
					</view>
				</view>
			</view>
			<view class="operations_container">
				<!-- 操作按钮的容器 -->
				<view class="unauthorizedinfo_container">
					<!-- 账号绑定 -->
				</view>
				<view>
					<!-- 基础操作 -->
				</view>
			</view>
		</view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				nickname: '未小羊',
				authorities: [
					{title: '学生', index: 0, class:"student_auth"},
					{title: '教务', index: 1, class:"teacher_auth"},
					{title: '从游坊管理员', index: 2, class:"cyf_admin_auth"},
					{title: '借用管理员', index: 3, class:"lending_admin_auth"},
					{title: '小程序管理员', index: 4, class:"mp_admin_auth"},
				],
				id: 2020999999
			}
		},
		onLoad() {

		},
		methods: {
			
		}
	}
</script>

<style>
	.img_top {
		/* 背景图片 */
		position: absolute;
		width: 750rpx;
		height: 400rpx;
		left: 0rpx;
		top: 0rpx;
	}
	
	.main_view {
		position: absolute;
		left: 0rpx;
		top: 400rpx;
		display: flex;
		flex-flow: row nowrap;
		justify-content: center;
		align-content: flex-start;
	}
	
	.avatar {
		/* 头像框 */
		position: absolute;
		width: 300rpx;
		height: 300rpx;
		left: 30rpx;
		top: -200rpx;
		
		border: 10rpx solid #660874;
		border-radius: 50%;
		box-sizing: border-box;
	}
	.nickname {
		/* 用户昵称 */
		position: absolute;
		width: 180rpx;
		height: 70rpx;
		left: 355rpx;
		top: -70rpx;
		
		font-family: Roboto;
		font-style: normal;
		font-weight: 800;
		font-size: 60rpx;
		line-height: 70rpx;
		
		color: #333;
		text-shadow:
			2rpx 0rpx 0rpx #FFFFFF,
			-2rpx 0rpx 0rpx #FFFFFF,
			0rpx 2rpx 0rpx #FFFFFF,
			0rpx -2rpx 0rpx #FFFFFF;
	}
	.student_auth {
		/* 学生 */
		width: 80rpx;
		height: 40rpx;
		
		background: #0087A9;
	}
	.teacher_auth {
		/* 教务 */
		width: 80rpx;
		height: 40rpx;
		
		background: #008C0E;
	}
	.cyf_admin_auth {
		/* 从游坊管理员 */
		width: 200rpx;
		height: 40rpx;
		
		background: #6C3974;
	}
	.lending_admin_auth {
		/* 借用管理员 */
		width: 170rpx;
		height: 40rpx;
		
		background: #0092A6;
	}
	.mp_admin_auth {
		/* 小程序管理员 */
		width: 200rpx;
		height: 40rpx;
		
		background: #EF5DA8;
	}
	.authorities_view {
		/* 所有权限标签的总体容器 */
		position: absolute;
		left: 350rpx;
		top: 10rpx;
		width: 400rpx;
		height: 200rpx;
		
		display: flex;
		flex-flow: row wrap;
		align-content: flex-start;
	}
	.authority_text {
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
	.authority_container {
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
		
		font-family: Roboto;
		font-style: normal;
		font-weight: 500;
		font-size: 32rpx;
		line-height: 42rpx;
		
		color: #333;
	}
	
	.unauthorizedinfo_container {
		/* 未授权的红色警告 */
		width: 690rpx;
		height: 120rpx;
		
		background: #FFD5D5;
		border-radius: 30rpx;
	}
	
	.operations_container {
		
		
		display: flex;
		flex-flow: row nowrap;
		align-content: center;
		justify-content: center;
	}
</style>
