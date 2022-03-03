<template>
	<view>
		<weiyang-section color="#112C9A" title="发起新的答疑" subtitle="请完整填写以下信息">
			<weiyang-forms ref="all_form" color="#112C9A" :title="['关键词','请输入五个字以内关键词']" :content="['问题正文','请解释问题详情']"
				:num="1" :group="basic_group" @submit="submit">
				<uni-forms ref="basic_form" :rules="basic_rules">
					<uni-forms-item label="问题主题" required name="tag">
						<uni-easyinput v-model="theme" placeholder="请简述核心问题" trim="both" />
					</uni-forms-item>
				</uni-forms>
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
				admin: false,
				theme: '',
				basic_rules: {
					tag: {
						rules: [{
							required: true,
							errorMessage: '请输入内容',
						}]
					}
				},
				basic_group:[{
					title: '',
					content: '',
					picurls: []
				}]
			}
		},
		methods: {
			submit() {
				uni.showLoading({
					title: '提交中',
					mask:true
				})
				this.$refs.basic_form.validate().then(() => {
					return this.$refs.all_form.submitAll()
				}).then(res => {
					return uni.request({
						url: app.globalData.url.backend + '/issue/',
						method: 'POST',
						header: {
							'content-type': 'application/json; charset=utf-8',
							'cookie': wx.getStorageSync('cookie')
						},
						data: {
							title: this.theme,
							tags: (this.admin?'#teacher;':'')+res[0].title,
							content: {
								text: res[0].content,
								urls: res[0].picurls
							}
						}
					})
				}).then(res=>{
					if(res.data.code!=0) utils.errInfo(res,res.data.errmsg)
					console.log(res)
					uni.hideLoading()
					uni.showToast({
						title:'提交成功',
						icon:'success',
						mask:true
					})
					setTimeout(uni.navigateBack,1000)
				}).catch(err => {
					uni.hideLoading()
					utils.errInfo(err, '表单填写有误')
				})
			}
		},
		onLoad(e) {
			this.admin = e.admin
		}
	}
</script>

<style>

</style>
