<template>
	<view>
		<weiyang-section color="#5800A6" :title="title" subtitle="请完整填写以下信息">
			<weiyang-forms ref="all_form" :group="basic_group" color="#5800A6" @submit="submit">
				<view class="paragraphs">活动基本信息</view>
				<uni-forms ref="basic_form" :modelValue="basic_data" :rules="basic_rules">
					<uni-forms-item label="活动名称" required name="title">
						<uni-easyinput v-model="basic_data.title" placeholder="请输入活动名称" trim="both" />
					</uni-forms-item>
					<uni-forms-item label="活动主题" required name="theme">
						<uni-easyinput v-model="basic_data.theme" placeholder="请输入活动主题" trim="both" />
					</uni-forms-item>
					<uni-forms-item label="主讲老师" required name="teacher">
						<uni-easyinput v-model="basic_data.teacher" placeholder="请输入老师姓名" />
					</uni-forms-item>
					<view style="margin:-10px 0 20px;">
						<uni-forms-item label="请上传老师照片" label-width='130' required></uni-forms-item>
						<view style="margin-top:-25px;">
							<uni-file-picker ref="teacher_pic" file-mediatype="image" mode="grid" :limit="1" />
						</view>
					</view>
					<uni-forms-item label="人数容量" required name="total">
						<uni-easyinput type="number" v-model="basic_data.total" placeholder="请输入人数容量" />
					</uni-forms-item>
					<uni-forms-item label="活动地点" required name="position">
						<uni-easyinput v-model="basic_data.position" placeholder="请输入活动地点" />
					</uni-forms-item>
					<uni-forms-item label="衔接方向" required name="subject">
						<uni-data-picker v-model="basic_data.subject" :localdata="subject_option" placeholder="请选择衔接方向">
						</uni-data-picker>
					</uni-forms-item>
					<uni-forms-item label="报名截止" required name="deadline">
						<uni-datetime-picker type="datetime" return-type="timestamp" v-model="basic_data.deadline"
							start="2022-1-1" end="2022-12-31" :clear-icon="false" :hideSecond="true"
							placeholder="请选择报名截止时间" />
					</uni-forms-item>
					<uni-forms-item label="活动时间" required name="holding_time">
						<uni-datetime-picker type="datetime" return-type="timestamp" v-model="basic_data.holding_time"
							start="2022-1-1" end="2022-12-31" :clear-icon="false" :hideSecond="true"
							placeholder="请选择活动举办时间" />
					</uni-forms-item>
				</uni-forms>
				<view class="paragraphs">活动详细介绍</view>
			</weiyang-forms>
		</weiyang-section>
	</view>
</template>

<script>
	const app = getApp()
	import utils from '../../../common/utils.js'
	export default {
		data() {
			return {
				id: 0,
				basic_data: {
					title: '',
					theme: '',
					subject: '',
					total: null,
					teacher: '',
					position: '',
					deadline: '',
					holding_time: '',
					'brief-intro': '',
					'detail-intro': {}
				},
				basic_group: [{
					title: '',
					content: '',
					picurls: []
				}],
				subject_option: [{
					text: "跨学科",
					value: "跨学科"
				}, {
					text: "建筑环境与能源应用工程",
					value: "建筑环境与能源应用工程"
				}, {
					text: "土木水利与海洋工程",
					value: "土木水利与海洋工程"
				}, {
					text: "环境工程",
					value: "环境工程"
				}, {
					text: "机械工程",
					value: "机械工程"
				}, {
					text: "测控技术与仪器",
					value: "测控技术与仪器"
				}, {
					text: "能源动力与工程",
					value: "能源动力与工程"
				}, {
					text: "工业工程",
					value: "工业工程"
				}, {
					text: "电气工程及其自动化",
					value: "电气工程及其自动化"
				}, {
					text: "微电子科学与工程",
					value: "微电子科学与工程"
				}, {
					text: "工程物理",
					value: "工程物理"
				}, {
					text: "材料科学与工程",
					value: "材料科学与工程"
				}, {
					text: "软件工程",
					value: "软件工程"
				}],
				basic_rules: {
					title: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					theme: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					subject: {
						rules: [{
							required: true,
							errorMessage: '请选择内容'
						}]
					},
					total: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					position: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					teacher: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					deadline: {
						rules: [{
							required: true,
							errorMessage: '请选择时间'
						}]
					},
					holding_time: {
						rules: [{
							required: true,
							errorMessage: '请选择时间'
						}]
					}
				}
			}
		},
		computed: {
			title() {
				return this.id == 0 ? '新建活动信息' : '修改活动信息'
			}
		},
		methods: {
			submit(e) {
				uni.showLoading({
					title: '提交中',
					mask: true
				})
				this.$refs.basic_form.validate().then(() => {
					return this.$refs.all_form.submitAll()
				}).then(res => {
					this.basic_data['detail-intro'] = res
					let what = this.$refs.teacher_pic.files[0]
					if (what) {
						return utils.uploadPic(what.name, what.url)
					} else {
						throw {data:{errmsg:'未选择老师照片'}}
					}
				}).then(res => {
					this.basic_data['brief-intro'] = res
					return uni.request({
						url: app.globalData.url.backend + '/lecture/',
						method: 'POST',
						header: {
							'content-type': 'application/json; charset=utf-8',
							'cookie': wx.getStorageSync('cookie')
						},
						data: this.basic_data
					})
				}).then(res => {
					uni.hideLoading()
					uni.showToast({
						title: '提交成功',
						icon: 'success',
						mask: true
					})
					console.log(this.basic_data)
					setTimeout(uni.navigateBack, 1000)
				}).catch(err => {
					uni.hideLoading()
					utils.errInfo(err, '表单填写有误')
				})

			}
		},
		onLoad(e) {
			if (e.id == 0) {
				uni.setNavigationBarTitle({
					title: '新建活动信息'
				})
			} else {
				uni.setNavigationBarTitle({
					title: '修改活动信息'
				})
			}
			this.id = e.id
		}
	}
</script>

<style>
	.paragraphs {
		width: 100%;
		text-align: center;
		font: bold 36rpx sans-serif;
		margin: -15rpx 0 20rpx;
	}
</style>
