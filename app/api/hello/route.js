import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'success',
    message: 'Welcome to SplitEase 2.0 API',
    version: '2.0.0',
    cloudSync: true
  });
}
