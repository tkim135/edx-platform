(function() {
    'use strict';
    var Metrics;
    var firstLoad = true;

    Metrics = (function() {
        function metrics($section) {
            this.$section = $section;
            this.$section.data('wrapper', this);
        }

        metrics.prototype.onClickTitle = function() {
            if (firstLoad) {
                loadGraphs();
                firstLoad = false;
            }
            $('#graph_reload').show();
            $('.metrics-header-container').show();
        };

        return metrics;
    }());

    window.InstructorDashboard.sections.Metrics = Metrics;
}).call(this);
