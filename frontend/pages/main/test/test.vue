<template>
	<view class="col-container">
		<weiyang-card :text="text" :pattern="11" :url="'dwdw'">{{'已报名25/20'}}</weiyang-card>
	</view>
</template>

<script>
    export default {
        data() {
            return {
                /* 不需要的内容可以返回空字符串 */
                text:{ 
					title: '从游坊第20讲',
					theme: '张三老师：关于怎么躺平的介绍',
					content: '4月20日 12：00南区9号楼地下活动空间，不见不散！',
					info: '2022-4-18 23：59 截止',
					tag: '可报名'
                }, 
                /* 请注意带上参数 */
                url:'../../dayi/index/index'
            }
        }
    }
</script>
