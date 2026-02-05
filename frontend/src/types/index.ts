// Типы для API "Умные листочки"

export interface Tag {
  id: number
  name: string
  slug: string
  usage_count: number
}

export interface CategoryParent {
  id: number
  name: string
  slug: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description: string
  parent: CategoryParent | null
  level: number
  is_parent: boolean
  full_path: string
  icon: string | null
  order: number
  worksheets_count: number
}

export interface CategoryTree extends Category {
  children: Category[]
}

export type GradeLevel = 'preschool' | 'kindergarten' | 'grade1' | 'grade2' | 'grade3' | 'grade4' | 'grade5'
export type Difficulty = 'easy' | 'medium' | 'hard'

export interface WorksheetListItem {
  id: number
  title: string
  slug: string
  description: string
  category_name: string
  category_slug: string
  category_path: string
  grade_level: GradeLevel
  difficulty: Difficulty
  thumbnail: string | null
  tags: Tag[]
  views_count: number
  downloads_count: number
  download_url: string
  created_at: string
}

export interface WorksheetDetail {
  id: number
  title: string
  slug: string
  description: string
  category: Category
  grade_level: GradeLevel
  difficulty: Difficulty
  thumbnail: string | null
  preview_image: string | null
  pdf_file: string
  tags: Tag[]
  views_count: number
  downloads_count: number
  download_url: string
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  count: number
  total_pages: number
  current_page: number
  page_size: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface SiteSettings {
  contact_email: string
  contact_phone: string
  header_text: string
  home_page_intro: string
  footer_text: string
  telegram_url: string
  worksheets_per_page: number
  show_stats: boolean
}

export interface StaticPage {
  id: number
  title: string
  slug: string
  body: string
  last_published_at: string
}
