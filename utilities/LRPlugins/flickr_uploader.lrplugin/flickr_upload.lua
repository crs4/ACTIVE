--[[----------------------------------------------------------------------------

ExportFilterProvider.lua
metaExportFilter Sample Plugin
ExportFilterProvider for the Metadata Export Filter sample plugin

Defines the dialog section to be displayed in the Export dialog and provides the
filter process before the photos are exported.

--------------------------------------------------------------------------------
ADOBE SYSTEMS INCORPORATED
 Copyright 2008 Adobe Systems Incorporated
 All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in accordance
with the terms of the Adobe license agreement accompanying it. If you have received
this file from a source other than Adobe, then your use, modification, or distribution
of it requires the prior written permission of Adobe.

------------------------------------------------------------------------------]]

local LrView = import 'LrView'
local bind = LrView.bind
local LrApplication = import 'LrApplication'
local LrDialogs = import 'LrDialogs'
local LrTasks = import 'LrTasks'
local catalog = LrApplication.activeCatalog()
local uploaderPath = "C:\\Program Files\\Flickr Uploadr\\Flickr Uploadr.exe" 
local LrShell = import 'LrShell'

local function setOnflickr( functionContext, exportContext )
   local photos = catalog:getTargetPhotos()
   local exportSession = exportContext.exportSession
   local renditions = exportSession:renditions(exportContext)

   -- set onflickt keyword
   catalog:withWriteAccessDo( "Set onflickr", function()
      local published_kw = catalog:createKeyword( "Published", {}, false, nil, true)
      local onflickr_kw = catalog:createKeyword( "onflickr", {}, false, published_kw, true)
      for _, photo in ipairs( photos ) do
         photo:addKeyword(onflickr_kw)
      end
--      local fn = photo:getFormattedMetadata( "fileName" )
--      photo:setRawMetadata( "caption", fn )
   end, {timeout=1} ) -- withWriteAccessDo
--   local message = "Overwrite caption field with the filename (without extension) for the "..#photosToUpdate.." target photos?"
--   result = LrDialogs.confirm( "Overwrite caption(s)?", message )

   -- start flickr uploader
   for _, rendition in renditions do
      rendition:waitForRender()
      LrShell.openFilesInApp({rendition.destinationPath}, uploaderPath)
   end

end -- function

return {
   hideSections = { 'video', 'fileNaming', 'metadata', 'watermarking' },
   processRenderedPhotos = setOnflickr
}

