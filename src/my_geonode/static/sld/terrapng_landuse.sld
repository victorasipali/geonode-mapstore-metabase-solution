<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
  xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
  xmlns="http://www.opengis.net/sld"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>TerraPNG Land Use Map</Name>
    <UserStyle>
      <Title>TerraPNG Land Use Map</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ChannelSelection>
              <GrayChannel>
                <SourceChannelName>1</SourceChannelName>
              </GrayChannel>
            </ChannelSelection>
            <ColorMap type="ramp">
              <ColorMapEntry color="#006400" quantity="1" label="Forest" opacity="1"/>
              <ColorMapEntry color="#8B4513" quantity="2" label="Non-Forest" opacity="1"/>
              <ColorMapEntry color="#FFD700" quantity="3" label="Agriculture" opacity="1"/>
              <ColorMapEntry color="#4169E1" quantity="6" label="Water" opacity="1"/>
              <ColorMapEntry color="#808080" quantity="9" label="Other" opacity="1"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>