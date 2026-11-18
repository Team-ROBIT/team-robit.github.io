// 사이트 전체 내비게이션 정의 (헤더 메가메뉴, 모바일 메뉴, 푸터, 페이지 경로 표기에 공통으로 사용)
import type { ImageMetadata } from 'astro';
import team from '../assets/assets_contest/team-robocup-humanoid.webp';
import rescue from '../assets/assets_contest/eclipse-2026-rescue.webp';
import safelab from '../assets/assets_contest/safelab-2026-gripper.webp';
import eclipseDefense from '../assets/assets_contest/eclipse-2026-defense.webp';
import srcirc from '../assets/assets_contest/team-src-irc.webp';
import tank from '../assets/assets_contest/defense-robot-003.webp';
import podium from '../assets/assets_awards/awards-2018-004.webp';
import banner from '../assets/assets_awards/awards-2016-002.webp';
import crowd from '../assets/assets_events/event-001.webp';
import invite from '../assets/assets_events/event-046.webp';
import team18 from '../assets/assets_members/members-18-team-1.webp';
import team19 from '../assets/assets_members/members-19-team-1.webp';
import team2 from '../assets/assets_awards/awards-2022-008.webp';
import tank1 from '../assets/assets_contest/defense-robot-001.webp';

export interface NavItem { label: string; href: string; meta?: string; image: ImageMetadata }
export interface NavSection { key: string; label: string; en: string; href: string; desc: string; items: NavItem[] }

export const sections: NavSection[] = [
  {
    key: 'overview', label: 'Overview', en: 'OVERVIEW · 소개', href: '/overview/information',
    desc: '이름의 의미와 창단 역사, 로빛이 하는 일을 소개합니다.',
    items: [
      { label: '로빛 소개', href: '/overview/information', meta: 'About', image: team2 },
      { label: 'History & Archive', href: '/overview/history', meta: '2006—', image: podium },
    ],
  },
  {
    key: 'contest', label: 'Contest', en: 'CONTEST · 대회', href: '/contest/participation',
    desc: 'RoboCup, SRC·IRC, 국방로봇경진대회 등 로빛이 참가한 국내외 대회의 기록입니다.',
    items: [
      { label: '참여 대회 전체', href: '/contest/participation', meta: '8종', image: podium },
      { label: 'RoboCup Humanoid', href: '/contest/robocup-humanoid', meta: 'Soccer', image: team },
      { label: 'RoboCup Rescue', href: '/contest/robocup-rescue', meta: 'Rescue', image: rescue },
      { label: 'SRCIRC 휴머노이드', href: '/contest/src-irc-humanoid', meta: 'Humanoid', image: srcirc },
      { label: 'IRC 매니퓰레이터 · SAFE LAB', href: '/contest/irc-manipulator', meta: '2026', image: safelab },
      { label: '국방로봇경진대회', href: '/contest/defense-robot', meta: 'Defense', image: eclipseDefense },
      { label: '극한로봇경진대회', href: '/contest/extreme-robot', meta: 'Extreme', image: rescue },
      { label: '수상 내역', href: '/contest/awards', meta: '295', image: podium },
    ],
  },
  {
    key: 'records', label: 'Records', en: 'RECORDS · 기록', href: '/events/participation',
    desc: '행사와 방송, 기사 스캔까지 로빛의 활동 기록을 모았습니다.',
    items: [
      { label: '참여 행사', href: '/events/participation', meta: '16', image: crowd },
      { label: '출연 방송', href: '/events/broadcast', meta: '7', image: invite },
      { label: '언론 보도', href: '/articles/press', meta: '74', image: podium },
    ],
  },
  {
    key: 'robots', label: 'Robots', en: 'ROBOTS · 로봇', href: '/robots/list',
    desc: '휴머노이드부터 재난구조 로봇까지, 역대 개발 로봇의 제원과 사진입니다.',
    items: [{ label: '로봇 목록', href: '/robots/list', meta: '57', image: tank1 }],
  },
  {
    key: 'people', label: 'People', en: 'PEOPLE · 단원', href: '/members/roster',
    desc: '1기부터 20기까지, 팀 사진과 주장, 인터뷰 영상을 기수별로 볼 수 있습니다.',
    items: [
      { label: '전체 명단', href: '/members/roster', meta: '20기', image: team },
      { label: '20기', href: '/members/20th', meta: '2026', image: team19 },
      { label: '19기', href: '/members/19th', meta: '2024', image: team19 },
      { label: '18기', href: '/members/18th', meta: '2023', image: team18 },
    ],
  },
];

export const contactHref = '/contact/contact';

/** 문서 경로(slug)로 소속 섹션과 경로 표기를 구한다. */
export function sectionOf(slug: string) {
  const top = slug.split('/')[0];
  const map: Record<string, { key: string; kicker: string }> = {
    overview: { key: 'overview', kicker: 'OVERVIEW' },
    contest: { key: 'contest', kicker: 'CONTEST' },
    events: { key: 'records', kicker: 'RECORDS' },
    articles: { key: 'records', kicker: 'RECORDS' },
    robots: { key: 'robots', kicker: 'ROBOTS' },
    members: { key: 'people', kicker: 'PEOPLE' },
    contact: { key: 'contact', kicker: 'CONTACT' },
  };
  return map[top] ?? { key: '', kicker: '' };
}
