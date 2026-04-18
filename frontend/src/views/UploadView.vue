<template>
  <div class="upload-page">
    <el-card class="upload-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="32" color="#409EFF"><Document /></el-icon>
          <h2>简历智能分析系统</h2>
          <p class="subtitle">上传 PDF 简历，AI 智能解析与岗位匹配</p>
        </div>
      </template>

      <el-upload
        class="upload-dragger"
        drag
        :auto-upload="false"
        :show-file-list="false"
        accept=".pdf"
        :on-change="handleFileChange"
        :disabled="isUploading"
      >
        <el-icon :size="48" color="#909399"><Upload /></el-icon>
        <div class="el-upload__text">
          <p>拖拽 PDF 文件到此处，或 <em>点击上传</em></p>
          <p class="upload-tip">仅支持单个 PDF 文件，大小不超过 10MB</p>
        </div>
      </el-upload>

      <div v-if="currentFile" class="file-info">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="文件名">
            <el-icon><Document /></el-icon>
            {{ currentFile.name }}
          </el-descriptions-item>
          <el-descriptions-item label="文件大小">
            {{ formatFileSize(currentFile.size) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <div v-if="isUploading" class="progress-section">
        <el-progress
          :percentage="uploadProgress"
          :status="uploadProgress === 100 ? 'success' : ''"
          :stroke-width="12"
          striped
        />
        <p class="progress-text">{{ uploadStatus }}</p>
      </div>

      <el-button
        v-if="currentFile && !isUploading"
        type="primary"
        size="large"
        class="upload-btn"
        @click="startUpload"
        :loading="isUploading"
      >
        <el-icon><Upload /></el-icon>
        开始上传
      </el-button>

      <el-button
        v-if="uploadResult"
        type="success"
        size="large"
        class="next-btn"
        @click="goToResult"
      >
        查看解析结果
        <el-icon><ArrowRight /></el-icon>
      </el-button>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, Upload, ArrowRight } from '@element-plus/icons-vue'
import { uploadResume } from '../api/resume'
import type { UploadFile } from 'element-plus'
import type { UploadResponse } from '../types'

const router = useRouter()

const currentFile = ref<File | null>(null)
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref('准备上传...')
const uploadResult = ref<UploadResponse | null>(null)

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleFileChange = (uploadFile: UploadFile) => {
  const rawFile = uploadFile.raw
  if (!rawFile) return

  if (rawFile.type !== 'application/pdf') {
    ElMessage.error('请上传 PDF 格式的文件')
    return
  }

  if (rawFile.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 10MB')
    return
  }

  currentFile.value = rawFile
  uploadResult.value = null
  uploadProgress.value = 0
}

const startUpload = async () => {
  if (!currentFile.value) return

  isUploading.value = true
  uploadStatus.value = '正在上传...'

  try {
    const result = await uploadResume(currentFile.value, (progress) => {
      uploadProgress.value = progress
      if (progress < 100) {
        uploadStatus.value = `正在上传... ${progress}%`
      } else {
        uploadStatus.value = '上传完成，正在解析...'
      }
    })

    uploadResult.value = result
    ElMessage.success('简历上传并解析成功！')
  } catch (error) {
    ElMessage.error('上传失败，请重试')
    uploadProgress.value = 0
  } finally {
    isUploading.value = false
  }
}

const goToResult = () => {
  if (uploadResult.value) {
    // 使用 sessionStorage 传递数据，避免刷新丢失
    sessionStorage.setItem('resumeData', JSON.stringify(uploadResult.value.data))
    router.push('/result')
  }
}
</script>

<style scoped lang="scss">
.upload-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.upload-card {
  width: 100%;
  max-width: 600px;
  border-radius: 16px;
}

.card-header {
  text-align: center;
  padding: 10px 0;

  h2 {
    margin: 12px 0 8px;
    color: #303133;
    font-size: 24px;
  }

  .subtitle {
    color: #909399;
    font-size: 14px;
    margin: 0;
  }
}

.upload-dragger {
  :deep(.el-upload-dragger) {
    padding: 40px 20px;
    border: 2px dashed #d9d9d9;
    border-radius: 8px;
    transition: all 0.3s;

    &:hover {
      border-color: #409EFF;
    }

    .el-upload__text {
      margin-top: 16px;

      em {
        color: #409EFF;
        font-style: normal;
        cursor: pointer;
      }
    }

    .upload-tip {
      color: #909399;
      font-size: 12px;
      margin-top: 8px;
    }
  }
}

.file-info {
  margin-top: 24px;
}

.progress-section {
  margin-top: 24px;
  text-align: center;

  .progress-text {
    margin-top: 12px;
    color: #606266;
    font-size: 14px;
  }
}

.upload-btn,
.next-btn {
  width: 100%;
  margin-top: 24px;
  height: 48px;
  font-size: 16px;
}

@media (max-width: 768px) {
  .upload-card {
    margin: 10px;
  }
}
</style>
