<template>
    <div class="single-input-dialog" v-if="visible">
        <el-dialog
            title=""
            :visible.sync="open"
            :show-close="true"
            width="350px"
            :before-close="handleClose"
            center>
                <el-form :show-message="false" :inline="true" :model="form" :rules="formRules" ref="form" >
                    <el-form-item label="" prop="single_input_text">
                        <el-input  v-model="form.single_input_text" :placeholder="label" ></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="fnAddNew('form')">添加</el-button>
                    </el-form-item>
                </el-form>
        </el-dialog>

        <div>
            <slot name="customContent"></slot>
        </div>
    </div>
</template>

<script>

    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "AddBranchDialog",
        props: {
            visible: {
                type: Boolean,
                required: true
            },
            label: {
                type: String,
                defalut: '',
            }
        },
        data() {
            return {
                open: false,
                form: {
                    single_input_text: ''
                },
                formRules: {
                    single_input_text: [
                        {required: true, message: '', trigger: 'change'}
                    ]
                }
            }
        },
        watch: {
            visible: function (newVal, oldVal) {
                if(newVal) {
                    this.open = true;
                }

            }
        },
        methods: {
            fnAddNew: function (form) {
                this.$refs[form].validate((valid) => {
                    if (valid) {
                        axios.post('api/add_new_branch', {
                            single_input_text: this.form.single_input_text
                        }).then(response => {
                            console.log(response);
                            this.$alert(response.data.resultMsg[0], '信息', {
                                 confirmButtonText: '确定',
                                 type: response.data.resultCode[0],
                            });
                        })
                        // this.$emit('addBranchCallback', this.form)
                    } else {
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                })
            },
            handleClose(done) {
                this.$emit('closeCallback', false);
                done();
            }
        },
        mounted() {
            this.open = true;
        }
    }
</script>

<style scoped>

</style>