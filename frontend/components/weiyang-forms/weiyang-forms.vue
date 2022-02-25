<template>
	<view style="padding: 30rpx;">
		<slot />
		<template v-for="(item,index) in data" :key="index">
			<uni-forms ref="form" :modelValue="item" :rules="rules">
				<uni-forms-item v-if="title[0]" :label="title[0]" required name="title">
					<uni-easyinput v-model="item.title" :placeholder="title[1]" trim="both" :maxlength="5" />
				</uni-forms-item>
				<uni-forms-item v-if="content[0]" :label="content[0]" required name="content">
					<uni-easyinput type="textarea" v-model="item.content" :placeholder='content[1]' trim="both"
						:maxlength="255" />
				</uni-forms-item>
				<view style="margin:-10px 0 20px;">
					<uni-forms-item label="可以附上至多3张图片" label-width='130'></uni-forms-item>
					<view style="margin-top:-25px;">
						<uni-file-picker ref="pic" file-mediatype="image" mode="grid" :limit="3" />
					</view>
				</view>
			</uni-forms>
			<view class="row-container" style="justify-content:flex-end;margin:-25rpx 0 100rpx">
				<weiyang-button type="green" v-if="data.length<num" @click="addPart(index)">新增节</weiyang-button>
				<weiyang-button type="red" v-if="data.length>1" @click="delPart(index)">删除节</weiyang-button>
			</view>
		</template>
	</view>
	<!-- 占位view -->
	<view style="height:60rpx;"></view>
	<view class="submitbar">
		<weiyang-button @click="submit">
			<view style="margin: 10rpx;">提交</view>
		</weiyang-button>
	</view>
</template>

<script>
	import utils from '../../common/utils.js'
	export default {
		name: 'weiyang-forms',
		emits: ['submit'],
		props: {
			title: {
				type: Array,
				default: ['节标题', '请输入节标题']
			},
			content: {
				type: Array,
				default: ['节正文', '请输入节正文']
			},
			color: {
				type: String,
				default: '#0087A9'
			},
			num: {
				type: Number,
				default: 5
			},
			group: {
				type: Array,
				default: [{
					title: '',
					content: '',
					picurls: []
				}]
			}
		},
		data() {
			return {
				// 基础表单数据
				data: this.group,
				// 表单验证规则
				rules: {
					title: {
						rules: [{
							required: this.title[0] && true,
							errorMessage: '请输入内容',
						}, {
							maxLength: 5,
							errorMessage: '至多输入 {maxLength} 个字符',
						}]
					},
					content: {
						rules: [{
							required: this.content[0] && true,
							errorMessage: '请输入内容',
						}]
					}
				}
			}
		},
		methods: {
			// 新增段落节
			addPart(e) {
				this.data.splice(e + 1, 0, {
					title: '',
					content: '',
					picurls: []
				})
			},
			// 删除段落节
			delPart(e) {
				this.data.splice(e, 1)
			},
			// 提交信息
			submit(e) {
				this.$emit('submit', e)
			},
			submitAll() {
				let length = this.data.length
				let ans1 = []
				// 验证表单
				for (let i = 0; i < length; i++) {
					ans1.push(this.$refs.form[i].validate())
				}
				return Promise.all(ans1).then(res => {
					let ans2 = []
					// 上传图片
					for (let i = 0; i < length; i++) {
						let ans3=[]
						for (let j in this.$refs.pic[i].files) {
							let what = this.$refs.pic[i].files[j]
							ans3.push(utils.uploadPic(what.name,what.url))
						}
						ans2.push(Promise.all(ans3))
					}
					return Promise.all(ans2)
				}).then(res=>{
					for (let i = 0; i < length; i++) {
						this.data[i].picurls=res[i]
					}
					return new Promise(resolve => {
						resolve(this.data)
					});
				})
			},
		}
	}
</script>

<style scoped>
	.submitbar {
		width: 90%;
		padding: 5%;
		background-color: #F3F3F3;

		position: fixed;
		bottom: 0;
		z-index: 10;
	}
</style>
