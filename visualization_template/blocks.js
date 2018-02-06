var blocks = {
  nodes: [
    {
      data: {
        id: 0
      },
      position: { x: 60, y: 0 },
      // classes: 'czerwony zielony'
    }, {
      data: {
        id: 1
      },
      position: { x: 120, y: 0 },
    },{
      data: {
        id: 2
      },
      position: { x: 180, y: 0 },
    }
  ],
  edges: [
    {
      data: {
        id: -1,
        source: 0,
        target: 1,
        srcID: 0
      },
      classes: 'edge'
    },{
     data: {
        id: -3,
        source: 0,
        target: 1,
        srcID: 1
      },
      classes: 'edge'
    },{
     data: {
        id: -4,
        source: 1,
        target: 2,
        srcID: 1
      },
      classes: 'edge'
     }]
};
