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
			<button v-if="index!=0" @click="delPart($event)" :data-index='index'>删去</button>
		</template>
			<button v-if="data.length<num" @click="addPart">新增</button>
			<button @click="submit()">提交</button>
	</view>
</template>

<script>
	export default {
		name: 'weiyang-forms',
		emits:['submit'],
		props: {
			title: {
				type: Array,
				default: ['标题','请输入标题']
			},
			content: {
				type: Array,
				default: ['正文','请输入正文']
			},
			color: {
				type: String,
				default: '#0087A9'
			},
			num: {
				type: Number,
				default: 5
			},
			group:{
				type: Array,
				default:[{
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
				rules:{
					title: {
						rules: [{
					        required: this.title[0] && true,
					        errorMessage: '请输入内容',
							},{
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
			// 新增段落节相关
			addPart(e){
				this.data.push({
					title: '',
					content: '',
					picurls: []
				})
			},
			delPart(e){
				let i=e.target.dataset.index
				this.data.splice(i,i)
			},
			// 提交信息
			submit(){
				let length=this.data.length
				let ans=[]
				for(let i=0;i<length;i++){
					ans.push(this.$refs.form[i].validate())
					console.log(this.$refs.pic[0].files[0].name,this.$refs.pic[0].files[0].url)
				}
				Promise.all(ans).then(res=>{
				    this.$emit('submit',this.data)
				}).catch(err =>{
				    console.log('表单错误信息：', err);
				})

			},
		}
	}
</script>

<style>
	
</style>
