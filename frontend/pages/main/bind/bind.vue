<template>
	<view>
		<weiyang-section title="身份信息绑定" subtitle="请仔细填写以下内容">
			<uni-forms ref="bindform" :modelValue="data" :rules="rules">
				<uni-forms-item label="身份" required name="admin">
					<uni-data-checkbox v-model="data.admin" :localdata="identity" selectedColor="#0087A9" @change="changeIdentity()">
					</uni-data-checkbox>
				</uni-forms-item>
				<uni-forms-item label="姓名" required name="name">
					<uni-easyinput v-model="data.name" placeholder="请输入姓名"></uni-easyinput>
				</uni-forms-item>
				<uni-forms-item label="学号" required name="id">
					<uni-easyinput v-model="data.id" placeholder="请输入学号" type="number"></uni-easyinput>
				</uni-forms-item>
				<uni-forms-item :label="class_label" required name="class">
					<uni-data-picker ref="child" v-model="data.class" :localdata="class_option" :popup-title="class_title"></uni-data-picker>
				</uni-forms-item>
			</uni-forms>
			<button @click="admitBind()">提交</button>
		</weiyang-section>
	</view>
</template>

<script>
	const app = getApp()
	export default {
		data() {
			return {
				data: {
					admin: 0,
					name: '',
					id: '',
					class: '',
				},
				rules: {
					name: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}]
					},
					id: {
						rules: [{
							required: true,
							errorMessage: '请输入内容'
						}, {
							minLength: 10,
							maxLength: 10,
							errorMessage: '学号为10位数字'
						}]
					},
					class: {
						rules: [{
							required: true,
							errorMessage: '请选择内容'
						}]
					}
				},
				identity: [{
					"value": 0,
					"text": "未央学生"
				}, {
					"value": 1,
					"text": "未央管理"
				}],
				classes: [{
					text: "2020级",
					value: "2020级",
					children: [{
						text: "未央-建环01",
						value: "未央-建环01"
					}, {
						text: "未央-水木01",
						value: "未央-水木01"
					}, {
						text: "未央-水木02",
						value: "未央-水木02"
					}, {
						text: "未央-环01",
						value: "未央-环01"
					}, {
						text: "未央-能动01",
						value: "未央-能动01"
					}, {
						text: "未央-能动02",
						value: "未央-能动02"
					}, {
						text: "未央-机械01",
						value: "未央-机械01"
					}, {
						text: "未央-精01",
						value: "未央-精01"
					}, {
						text: "未央-工01",
						value: "未央-工01"
					}, {
						text: "未央-电01",
						value: "未央-电01"
					}, {
						text: "未央-微01",
						value: "未央-微01"
					}, {
						text: "未央-软件01",
						value: "未央-软件01"
					}, {
						text: "未央-工物01",
						value: "未央-工物01"
					}, {
						text: "未央-材01",
						value: "未央-材01"
					}],
				}, {
					text: "2021级",
					value: "2021级",
					children: [{
						text: "未央-建环11",
						value: "未央-建环11"
					}, {
						text: "未央-水木11",
						value: "未央-水木11"
					}, {
						text: "未央-水木12",
						value: "未央-水木12"
					}, {
						text: "未央-环11",
						value: "未央-环11"
					}, {
						text: "未央-能动11",
						value: "未央-能动11"
					}, {
						text: "未央-能动12",
						value: "未央-能动12"
					}, {
						text: "未央-机械11",
						value: "未央-机械11"
					}, {
						text: "未央-精11",
						value: "未央-精11"
					}, {
						text: "未央-工11",
						value: "未央-工11"
					}, {
						text: "未央-电11",
						value: "未央-电11"
					}, {
						text: "未央-微11",
						value: "未央-微11"
					}, {
						text: "未央-软件11",
						value: "未央-软件11"
					}, {
						text: "未央-工物11",
						value: "未央-工物11"
					}, {
						text: "未央-材11",
						value: "未央-材11"
					}, {
						text: "未央-材12",
						value: "未央-材12"
					}, {
						text: "未央-材13",
						value: "未央-材13"
					}],
				}],
				apartments: [{
					text: "未央团工委",
					value: "未央团工委"
				}, {
					text: "党建辅导员",
					value: "党建辅导员"
				}, {
					text: "带班辅导员",
					value: "带班辅导员"
				}, {
					text: "未央教务",
					value: "未央教务"
				}],
			}
		},
		computed: {
			class_label() {
				return this.data.admin == 0 ? '班级' : '部门'
			},
			class_title() {
				return this.data.admin == 0 ? '请选择班级' : '请选择部门'
			},
			class_option() {
				return this.data.admin == 0 ? this.classes : this.apartments
			}
		},
		methods: {
			// 身份选择转变
			changeIdentity(){
				this.$refs.child.clear()
			},
			// 提交绑定信息
			admitBind() {
				console.log(this.data)
				this.$refs.bindform.validate().then(res => {
					return uni.request({
						header: {
							'content-type': 'application/json; charset=utf-8',
							'cookie': wx.getStorageSync('cookie')
						},
						url: app.globalData.url.backend + '/bind/',
						method: 'POST',
						data: {
							id: this.data.id,
							name: this.data.name,
							clazz: this.data.class
						}
					})
				}).then(res => {
					console.log(res)
					// 提示绑定成功，返回上一页，刷新
				}).catch(res => {
					console.log(res)
					// 提示绑定失败并显示原因
				})
			}
		}
	}
</script>

<style>

</style>
