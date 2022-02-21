<template>
	<view>
		<weiyang-section color="#5800A6" :title="title" subtitle="请完整填写以下信息">
			<weiyang-forms color="#5800A6" @submit="submit">
				<view class="paragraphs">活动基本信息</view>
				<uni-forms ref="basicform" :modelValue="basic_data" :rules="rules">
					<uni-forms-item label="活动名称" required name="title">
						<uni-easyinput v-model="basic_data.title" placeholder="请输入活动名称" trim="both" />
					</uni-forms-item>
					<uni-forms-item label="活动主题" required name="theme">
						<uni-easyinput v-model="basic_data.theme" placeholder="请输入活动主题" trim="both" />
					</uni-forms-item>
					<uni-forms-item label="主讲老师" required name="total">
						<uni-easyinput v-model="basic_data.teacher" placeholder="请输入老师姓名" />
					</uni-forms-item>
					<view style="margin:-10px 0 20px;">
						<uni-forms-item label="请上传老师照片" label-width='130' required></uni-forms-item>
						<view style="margin-top:-25px;">
							<uni-file-picker ref="teacher-pic" file-mediatype="image" mode="grid" :limit="1" />
						</view>
					</view>
					<uni-forms-item label="人数容量" required name="total">
						<uni-easyinput type="number" v-model="basic_data.total" placeholder="请输入人数容量" />
					</uni-forms-item>
					<uni-forms-item label="衔接方向" required name="subject">
						<uni-data-picker v-model="basic_data.subject" :localdata="subject_option" placeholder="请选择衔接方向">
						</uni-data-picker>
					</uni-forms-item>
					<uni-forms-item label="报名截止" required name="deadline">
						<uni-datetime-picker type="datetime" return-type="timestamp" v-model="basic_data.deadline"
						start="2022-1-1" end="2022-12-31" :clear-icon="false" :hideSecond="true" placeholder="请选择报名截止时间"/>
					</uni-forms-item>
					<uni-forms-item label="活动时间" required name="holding_time">
						<uni-datetime-picker type="datetime" return-type="timestamp" v-model="basic_data.holding_time"
						start="2022-1-1" end="2022-12-31" :clear-icon="false" :hideSecond="true" placeholder="请选择活动举办时间"/>
					</uni-forms-item>
				</uni-forms>
				<view class="paragraphs">活动详细介绍</view>
			</weiyang-forms>
		</weiyang-section>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: 0,
				basic_data: {
					title: '',
					theme: '',
					subject: '',
					total: 0,
					teacher: '',
					deadline: '',
					holding_time: '',
					'detail-intro': {}
				},
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
				}]
			}
		},
		computed: {
			title() {
				return this.id == 0 ? '新建活动信息' : '修改活动信息'
			}
		},
		methods: {
			submit(e) {
				this.basic_data['detail-intro']=e
				console.log(this.basic_data)
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
	.paragraphs{
		width: 100%;
		text-align: center;
		font: bold 36rpx sans-serif;
		margin: -20rpx 0 20rpx;
	}
</style>
