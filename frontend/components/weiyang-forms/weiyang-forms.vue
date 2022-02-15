<template>
	<view style="padding: 30rpx;">
		<uni-forms ref="baseForm" :modelValue="baseFormData">
			<slot/>
			<uni-forms-item label="姓名" required>
				<uni-easyinput v-model="baseFormData.name" placeholder="请输入姓名" />
			</uni-forms-item>
			<uni-forms-item label="年龄" required>
				<uni-easyinput v-model="baseFormData.age" placeholder="请输入年龄" />
			</uni-forms-item>
			<uni-forms-item label="性别" required>
				<uni-data-checkbox v-model="baseFormData.sex" :localdata="sexs" />
			</uni-forms-item>
			<uni-forms-item label="自我介绍">
				<uni-easyinput type="textarea" v-model="baseFormData.introduction" placeholder="请输入自我介绍" />
			</uni-forms-item>
			<uni-forms-item label="日期时间">
				<uni-datetime-picker type="datetime" return-type="timestamp" v-model="baseFormData.datetimesingle" />
			</uni-forms-item>
		</uni-forms>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-forms',
		data() {
			return {
				// 基础表单数据
				baseFormData: {
					name: '',
					age: '',
					introduction: '',
					sex: 2,
					hobby: [5],
					datetimesingle: 1627529992399
				},
				sexs: [{
					text: '男',
					value: 0
				}, {
					text: '女',
					value: 1
				}, {
					text: '保密',
					value: 2
				}],
			}
		},
	}
</script>

<style>

</style>
