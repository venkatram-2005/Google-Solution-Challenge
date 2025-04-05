import React from 'react'
import SideBar from './_components/SideBar'
import DashboardHeader from './_components/DashboardHeader'

function DashboardLayout({children}) {
  return (
    <div className='h-screen'>
      <div className='md:w-64 hidden md:block fixed'>
        <SideBar />
      </div>
      <div className='md:ml-64'>
        <DashboardHeader />
        <div className='p-10'>
            {children}
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout